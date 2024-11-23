<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize form inputs
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $subject = htmlspecialchars($_POST['subject']);
    $message = htmlspecialchars($_POST['message']);

    // Email address that will recieve email
    $to = "person@example.com";
    $headers = "From: $email\r\n";
    $body = "Name: $name\nEmail: $email\nSubject: $subject\nMessage:\n$message";

    // Attempt to send the email
    if (mail($to, $subject, $body, $headers)) {
        // Alert success and redirect back to the contact page
        echo "<script>
                alert('Message sent successfully!');
                window.location.href='contact.html';
              </script>";
    } else {
        // Alert failure and redirect back to the contact page
        echo "<script>
                alert('Failed to send the message. Please try again.');
                window.location.href='contact.html';
              </script>";
    }
}
?>
