<?php include 'user.php' ?>

<?php
    

  if($user_data['user_type'] == "doctor") 
  {
    include 'dashboard.html';
 
  } else 
  {
    echo $user_data['user_type'];
    include "errorpage.html";
  }

?>