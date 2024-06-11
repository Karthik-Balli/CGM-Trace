<?php

session_start();

    include("connection.php");
    include("functions.php");

    if($_SERVER['REQUEST_METHOD'] == "POST")
    {

        //something was posted
        $user_name = $_POST['user_name'];
        $password = $_POST['password'];

        if(!empty($user_name) && !empty($password) && !is_numeric($user_name))
        {
            //read from database 
            $query = "select * from users where user_name = '$user_name' limit 1";
            $result = mysqli_query($con, $query);
            if($result)
            {
                if($result)
                {
                    if($result && mysqli_num_rows($result) > 0)
                    {
                        $user_data = mysqli_fetch_assoc($result);

                        if($user_data['password'] === $password) 
                        {
                            $_SESSION['user_id'] = $user_data['user_id'];
                        header("Location: index.html");
                        die;
                        }
                    }              
               }
               echo "<script>alert('Wrong username or password!')</script>" ;
           }else 
           {
            echo "<script>alert('Wrong username or password!')</script>" ;
           }

        }
    }

?>


<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Login Page</title>

	 
    
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
    height: 480px;
    width: 390px;
    background-color: rgba(255,255,255,0.13);
    position: absolute;
    transform: translate(-50%,-50%);
    top: 55%;
    left: 50%;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 40px rgba(8,7,16,0.6);
    padding: 50px 35px;
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
input{
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
::placeholder{
    color: #e5e5e5;
}
input:hover{
	background-color: #190482;
}
#button{
    margin-top: 40px;
    width: 100%;
    background-color: #ffffff;
    color: #080710;
    padding: 15px 0;
    font-size: 18px;
    font-weight: 600;
    border-radius: 5px;
    cursor: pointer;
}
.signup{
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
        <h3>Login Here</h3>

        <label for="username">Username</label>
        <input type="text" placeholder="Username" id="username" name="user_name">

        <label for="password">Password</label>
        <input type="password" placeholder="Password" id="password" name="password">

        <input id="button" type="submit" value="Login" />
        <div class="signup">
        	<h5>If you don't have an Account ? &nbsp<a href="signup.php"><u> Sign Up </u></a></h5>
        </div>
    </form>

</body>
</html>