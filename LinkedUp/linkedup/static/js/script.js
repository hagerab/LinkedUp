document.getElementById('getPostsBtn').addEventListener('click', getPosts);

async function getPosts() {
    try {
        const response = await fetch('/api/posts');
        const posts = await response.json();
        
        const postsList = document.getElementById('postsList');
        postsList.innerHTML = ''; // Clear any existing posts

        posts.forEach(post => {
            const postDiv = document.createElement('div');
            postDiv.classList.add('post');
            postDiv.innerHTML = `<h3>${post.title}</h3><p>${post.content}</p>`;
            postsList.appendChild(postDiv);
        });
    } catch (error) {
        console.error('Error fetching posts:', error);
    }
}
