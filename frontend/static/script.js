"use strict"

const FETCH_ADDRESS = "/api/data";

let postManager = {
	
	async fetchData(address=FETCH_ADDRESS) {
		const response = await fetch(address);
		let posts = await response.json();
		return posts;
	},

	createPost(author,postContent,postDate){
		const pageCenter = document.querySelector("div.center-style");
		const newPost = document.createElement("article");
		newPost.className = "center-post";
		
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
	},

	async renderAll() {
		const posts = await this.fetchData();
		for (let post of posts) {
			this.createPost(post.author,post.post_content,post.post_date);
		}
				
	}

}

postManager.renderAll();
