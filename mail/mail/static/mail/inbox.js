document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', () => {
    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value;
    console.log(recipients, subject, body);
    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value;
    send_mail(recipients, subject, body);
  });
  //by default
  load_mailbox('inbox')
});

function send_mail(recipients, subject, body) {
  console.log(recipients, subject, body);
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    document.querySelector('#message').innerHTML = result.error;
    timestamp(2000);
  });
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-properties').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#message').style.display = 'block';

  document.querySelector('#message').innerHTML = '';
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message').style.display = 'none';
  document.querySelector('#email-properties').style.display = 'none';

  fetch(`emails/${mailbox}`).then(response => response.json())
  .then(emails => {
    if(emails){
      var table = document.createElement('table');
      table.className = 'table table-bordered';
      emails.forEach(function(element) {
        const button_archive = document.createElement('button');
        button_archive.id = 'archive';
        button_archive.innerText = 'archive';

        const button_unarchive = document.createElement('button');
        button_unarchive.id = 'unarchive';
        button_unarchive.innerText = 'unarchive';

        var row = table.insertRow(-1);
        cell1 = row.insertCell(0);
        cell1.className = 'col-3';
        cell2 = row.insertCell(1);
        cell2.className = 'col-4';
        cell3 = row.insertCell(2);
        cell3.className = 'col-3';
        cell4 = row.insertCell(3);
        cell4.className = 'col-1';
        console.log(element.recipients);
        console.log(mailbox);
        if (mailbox == 'sent') {
          cell1.innerHTML = element.recipients;
          cell2.innerHTML = element.subject;
          cell3.innerHTML = element.timestamp;
        } else if (mailbox == 'archive'){
          cell1.innerHTML = element.sender;
          cell2.innerHTML = element.subject;
          cell3.innerHTML = element.timestamp;
          cell4.appendChild(button_unarchive);
        } else {
          cell1.innerHTML = element.sender;
          cell2.innerHTML = element.subject;
          cell3.innerHTML = element.timestamp;
          cell4.appendChild(button_archive);
        }
        cell1.addEventListener('click', function() {
          show_mail(element.id);
        });
        cell2.addEventListener('click', function() {
          show_mail(element.id);
        });
        cell3.addEventListener('click', function() {
          show_mail(element.id);
        });
        button_archive.addEventListener('click', () => {
          fetch(`/emails/${element.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
          .then(() => {
            load_mailbox('inbox');
          })
        })
        button_unarchive.addEventListener('click', () =>{
          fetch(`/emails/${element.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
          .then(() => {
            load_mailbox('inbox');
          })
        });
        if (element.read === false){
          row.style.backgroundColor = 'LightGray';
        }
        document.querySelector('#emails-view').append(table);
      });
    }
  })
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function show_mail(mail_id){
  document.querySelector('#email-properties').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message').style.display = 'none';
  const reply_button = document.createElement('button');
  reply_button.className = 'btn btn-primary';
  reply_button.innerText = 'Reply';
  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(email => {
    fetch(`/emails/${mail_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
    document.querySelector('#email-sender').innerHTML = `<strong>From: </strong> ${email.sender}`;
    document.querySelector('#email-recipients').innerHTML = `<strong>To: </strong> ${email.recipients}`;
    document.querySelector('#email-subject').innerHTML = `<strong>Subject: </strong> ${email.subject}`;
    document.querySelector('#email-timestamp').innerHTML = `<strong>Timestamp: </strong> ${email.timestamp}`;
    document.querySelector('#email-body').innerHTML = `${email.body}`;
    reply_button.addEventListener('click', () => {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: \n "${email.body}" \n`;
    });
  })
  document.querySelector('#reply-placeholder').appendChild(reply_button);
}