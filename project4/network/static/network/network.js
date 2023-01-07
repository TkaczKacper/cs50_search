function getCurrentUrl() {
      return window.location.pathname
}

document.addEventListener('DOMContentLoaded', function () {
      const url = getCurrentUrl()
      
      if (url === '/following') {
            document.querySelector('#new-post-view').style.display = 'none';
            document.querySelectorAll('h1')[1].innerHTML = 'Following users posts:'
      }
      
      document.querySelectorAll('.edit_post_button').forEach(element => {
            element.addEventListener('click', () => {
                  const post_id = element.id;
                  document.querySelector(`#post_content_edit_${post_id}`).style.display = 'block';
                  document.querySelector(`#post_content_view_${post_id}`).style.display = 'none';
            });
      });
      document.querySelectorAll('.cancel_edit_button').forEach(element => {
            element.addEventListener('click', () => {
                  const post_id = element.id;
                  document.querySelector(`#post_content_edit_${post_id}`).style.display = 'none';
                  document.querySelector(`#post_content_view_${post_id}`).style.display = 'block';
            });
      });
      document.querySelectorAll('.save_post_button').forEach(element => {
            element.addEventListener('click', (event) => {
                  event.preventDefault();
                  const content = document.querySelector(`#post${element.id}_content`).value;
                  console.log(content);
                  fetch(`/edit/${element.id}`, {
                        method: 'UPDATE',
                        body: JSON.stringify({
                              content: content
                        })
                  })
                  .then(() => {
                        document.querySelector(`#post_content_edit_post${element.id}`).style.display = 'none';
                        document.querySelector(`#post_content_view_post${element.id}`).style.display = 'block';
                        document.querySelector(`#post_content_view_post${element.id}`).innerHTML = content;
                  });
            });
      });
      document.querySelectorAll('.liked').forEach(element => {
            element.addEventListener('click', unlike(element));
      });
      document.querySelectorAll('.not_liked').forEach(element => {
            element.addEventListener('click', () => {
                  console.log(`unclicked ${element.id}`)
            });
      });
      //by default edit view hidden
      document.querySelectorAll('.post_content_edit').forEach(element => {
            element.style.display = 'none';
      });
});

function unlike(element) {
      const mainDiv = document.querySelector(`#post${element.id}_likes`);
      const divToRemove = document.querySelector(`#post${element.id}_likes`).children[0];
      divToRemove.remove();
      const div_to_insert = document.createElement('div');
      div_to_insert.id = element.id;
      div_to_insert.className = 'not_liked';
      const likes_count = mainDiv.innerHTML - 1;
      mainDiv.innerHTML = '';
      mainDiv.appendChild(div_to_insert);
      mainDiv.innerHTML += likes_count;
}