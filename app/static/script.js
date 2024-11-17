function openSidebar() {
  document.getElementById("mySidebar").style.width = "250px";
  document.querySelector(".main-content").style.marginLeft = "250px";
}

function closeSidebar() {
  document.getElementById("mySidebar").style.width = "0";
  document.querySelector(".main-content").style.marginLeft = "0";
}

function checkLoginStatus() {
  fetch('/is_logged_in', { method: 'GET' })
      .then(response => response.json())
      .then(data => {
          if (data.loggedIn) {
              window.location.href = '/matches';
          } else {
              window.location.href = '/login';
          }
      })
      .catch(error => {
          console.error('Error checking login status:', error);
          alert('An error occurred. Please try again later.');
      });
}