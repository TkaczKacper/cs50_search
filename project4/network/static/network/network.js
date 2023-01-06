function getCurrentUrl() {
      return window.location.pathname
}

document.addEventListener('DOMContentLoaded', function () {
      const url = getCurrentUrl()
      
      if (url === '/following') {
            document.querySelector('#new-post-view').style.display = 'none';
            document.querySelectorAll('h1')[1].innerHTML = 'Following users posts:'
      }
})