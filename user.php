<?php 

	
	include("connection.php");
	include("functions.php");

	$user_data = check_login($con);
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title></title>
</head>
<body>
	<h4 style="color: #080710;">Welcome, <b> <?php echo $user_data['user_name'] ?></b></h4>
</body>
</html>