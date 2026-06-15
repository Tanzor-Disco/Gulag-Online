import requests
import bs4 

TELEGRAM_CHANNELS = [
        "https://t.me/s/vv_volodin",
        "https://t.me/s/medvedev_telegram",
        "https://t.me/s/margaritasimonyan"
]

class TelegramParser:
    def __init__(self):
        self.subjects_list = TELEGRAM_CHANNELS
        self.curr_subject_idx = 0


    def _get_soup(self,telegram_url):
        request = requests.get(telegram_url)
        soup = bs4.BeautifulSoup(request.text,features="html.parser")
        return soup

    def _get_author_name(self,subject_url):
        soup = self._get_soup(subject_url)
        author_tag = soup.find("a",class_ = "tgme_widget_message_owner_name")
        assert author_tag is not None
        author_name = author_tag.get_text()
        return author_name

    def _get_post_id(self,tag):
        post_id = tag.get("data-post")
        return post_id

    def _get_post_text(self,tag):
            text_tag= tag.select_one("div.tgme_widget_message_text.js-message_text")
            if text_tag is None:
                return None
            assert text_tag is not None
            text = text_tag.get_text(separator=" ",strip=True)
            return text

    def _get_post_date(self,tag):
        time = tag.select_one("time.time")
        date = time.get("datetime").split("T")[0]
        return date

    def get_parsed_data(self):
        subject_url = self.subjects_list[self.curr_subject_idx]
        soup = self._get_soup(subject_url)

        parsed_data = []
        author_name = self._get_author_name(subject_url)

        post_tags = soup.select("div.tgme_widget_message.text_not_supported_wrap.js-widget_message")
        for tag in post_tags:
            text = self._get_post_text(tag)
            if text is None:
                continue

            date =self._get_post_date(tag)
            post_id = self._get_post_id(tag)
            post_dict = {"id":post_id,"date":date,"author":author_name,"text":text}
            parsed_data.append(post_dict)
        
        #switching the subject to diversify the content
        self.curr_subject_idx = (self.curr_subject_idx + 1) % len(self.subjects_list)
        return parsed_data


if __name__ == "__main__":
    test = TelegramParser()
    post_list = test.get_parsed_data()
    print(post_list)
