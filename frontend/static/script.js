"use strict"

const FETCH_ADDRESS = "/api/data";

let postManager = {
	postCounter:0,
	observerCounter:0,
	observer:null,

	async fetchData() {
		const address = `${FETCH_ADDRESS}/?section=${this.observerCounter}`
		const response = await fetch(address);
		let posts = await response.json();
		return posts;
	},

	createPost(author,postContent,postDate,isObserved) {
		const pageCenter = document.querySelector("div.center-style");
		const newPost = document.createElement("article");
		newPost.className = "center-post";
		newPost.setAttribute("number",this.postCounter);
		this.postCounter+=1;

				
		let imageName = null;
		switch (author) {
			case "Вячеслав Володин":
				imageName = "volodin.jpeg";
				break;

			case "Дмитрий Медведев":
				imageName = "medvedev.jpeg";
				break;

			case "Маргарита Симоньян":
				imageName = "simonan.jpeg"
				break;

			case "Александр Дугин":
				imageName = "dugin.jpg"
				break;

			default:
				console.warn(`None of the images matched ${author}`);
		}

		newPost.innerHTML = `
			<header class = "center-post-header"> 

				<span>${author}</span>
				<img class = "center-post-photo" src = "../images/${imageName}">

			</header>

			<p>${postDate}</p>
			<p>${postContent}</p>
		`	
		pageCenter.append(newPost);

		if (isObserved) {
			this.observer.observe(newPost);
		}
	},
	
	async getPosts (entries) {
		if (this.observer === null) {
			console.error("Observer is not initialized");
			return []
		} 
                                                  
		let obs_obj = entries[0].target;
		this.observer.unobserve(obs_obj);
														  
		const posts = await this.fetchData();
		return posts;
	},

	async renderPosts(entries) {
		if (!entries[0].isIntersecting) return // callback can be called with a tag not intersecting the viewport

		const posts = await this.getPosts(entries);
		for (const [post_idx,post] of posts.entries()) {
			const half = Math.floor(posts.length/2);
			const isObserved = post_idx == half;
			const convDate = new Date(post.post_date).toLocaleDateString('ru-RU');
			this.createPost(post.author,post.post_content,convDate,isObserved);
		}

		this.observerCounter+=1;
	},

	startObserving(tag) {
		if (this.observer === null) {
			console.error("Observer is not initialized");
			return 
		} 
		this.observer.observe(tag);
	}

}


const observer_options = {
	root:null,
	rootMargin: "0px",
	scrollMargin: "0px",
	threshold: 1.0,
};

postManager.observer = new IntersectionObserver(postManager.renderPosts.bind(postManager),observer_options);
const firstObserved = document.querySelector("div.page-center");
postManager.startObserving(firstObserved);


