<?php
session_start();

    include("connection.php");
    include("functions.php");

    if($_SERVER['REQUEST_METHOD'] == "POST")
    {

        //something was posted
        $user_name = $_POST['user_name'];
        $password = $_POST['password'];
        $user_type = $_POST['user_type'];

        if(!empty($user_name) && !empty($password) && !empty($user_type) && !is_numeric($user_name))
        {

            $read_query = "select * from users where user_name = '$user_name' limit 1;";
            $result = mysqli_query($con, $read_query);
            $user_data = mysqli_fetch_assoc($result);
            if($user_data['user_name'] == $user_name)
            {
                echo "<script>alert('Username already used, Please try another one')</script>";
            } else
            {
                // save to database 
                $user_id = random_num(20);
                $query = "insert into users (user_id, user_name, password, user_type) values ('$user_id', '$user_name', '$password', '$user_type')";

                mysqli_query($con, $query);

                header("Location: login.php");
                die;
            }
        }else 
        {
            echo "Please enter some valid information!";
        }       

    }

?>


<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Signup Page</title>

	 
    
    <!--Stylesheet-->
    <style media="screen">
      *,
*:before,
*:after{
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}
body{
    background-color: #7743DB;

}
.background{
    width: 430px;
    height: 520px;
    position: absolute;
    transform: translate(-50%,-50%);
    left: 50%;
    top: 50%;
}
.background .shape{
    height: 200px;
    width: 200px;
    position: absolute;
    border-radius: 50%;
}
.shape:first-child{
    background: linear-gradient(
        #1845ad,
        #23a2f6
    );
    left: -80px;
    top: -80px;
}
.shape:last-child{
    background: linear-gradient(
        to right,
        #ff512f,
        #f09819
    );
    right: -30px;
    bottom: -80px;
}
.navbar{
	width: 100%;
	height: 45px;
	background-color: #f5f5f5;
	font-family: sans-serif;
	align-items: center;
	position: absolute;
	font-size: 20px;
	overflow: hidden;
}
.nav-left{
	position: absolute;
	top: 10px;
	left: 18px;
}
.nav-right a{
	color: #080710;
	text-align: center;
	padding: 15px 25px;
	text-decoration: none;
	font-size: 17px;
}
.navbar a:hover {
  background-color: #080710;
  color: #f5f5f5;
}
.nav-right{
	display: flex;
	float:right;
}
form{
    height: 560px;
    width: 390px;
    background-color: rgba(255,255,255,0.13);
    position: absolute;
    transform: translate(-50%,-50%);
    top:  60%;
    left: 50%;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 40px rgba(8,7,16,0.6);
    padding: 40px 35px;
}
form *{
    font-family: 'Poppins',sans-serif;
    color: #ffffff;
    letter-spacing: 0.5px;
    outline: none;
    border: none;
}
form h3{
    font-size: 32px;
    font-weight: 500;
    line-height: 42px;
    text-align: center;
}

label{
    display: block;
    margin-top: 30px;
    font-size: 16px;
    font-weight: 500;
}
input, select{
    display: block;
    height: 50px;
    width: 100%;
    background-color: rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0 10px;
    margin-top: 8px;
    font-size: 14px;
    font-weight: 300;
}
option{
    color: #190482;
}
::placeholder{
    color: #e5e5e5;
}
input:hover{
	background-color: #190482;
}
#button{
    margin-top: 30px;
    width: 100%;
    background-color: #ffffff;
    color: #080710;
    padding: 10px 0;
    font-size: 18px;
    font-weight: 600;
    border-radius: 5px;
    cursor: pointer;
}
.login{
	margin-top: 15px;
}

    </style>

</head>
<body>

	<div class="background">
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <div class="navbar">
    	<div class="nav-left">
    		Health Checkup
    	</div>
    	<div class="nav-right">
    		<a href="login.php">Login</a>
    		<a href="signup.php">Signup</a>
    	</div>
    </div>
    <form method="post">
        <h3>Signup Here</h3>

        <label for="username">Username</label>
        <input type="text" placeholder="Username" id="username" name="user_name">

        <label for="password">Password</label>
        <input type="password" placeholder="Password" id="password" name="password">

        <label for="usertype">Select User type</label>
        <select id="usertype" name="user_type">
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
        </select>

        <input id="button" type="submit" value="Signup" />
        <div class="login">
        	<h5>Back to Login page ? &nbsp<a href="Login.php"><u> Login </u></a></h5>
        </div>
    </form>

</body>
</html>