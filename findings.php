<?php
  session_start();
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Findings</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {
      background-image: url("https://img.freepik.com/free-photo/hand-holding-blood-glucose-meter-measuring-blood-sugar-background-is-stethoscope-chart-file_1387-931.jpg");
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
    }

    .container {
      background-color: rgba(255, 255, 255, 0.9);
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
    }
  </style>

</head>
<body>

  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <a class="navbar-brand" href="#">Glucose Analysis</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <a class="nav-link" href="index.html">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="info.html">Info</a>
        </li>
        <li class="na-link">
          <a class="nav-link" href="num.html">Metrics</a>
        </li>
      </ul>
    </div>
  </nav>

  <?php include 'user.php' ?>

  <?php

  if($user_data['user_type'] == "doctor") 
  {
    echo "<div class='container mt-5'>";
    echo "<h3> <div id='demo' > </div></h3>";
    echo "</div>";
  } else 
  {
    echo "<div class='container mt-5'>";
    echo "This page is authorized for Doctors only !";
    echo "</div>";
  }

?>


	<script>

    var mg = 0;
    var sd = 0;
    var sdr = 0;
    var gv = 0;
    var tar = 0;
    var tar1 = 0;
    var tar2 = 0;
    var tbr = 0;
    var tbr1 = 0;
    var tbr2 = 0;
    var tir = 0;
    var madd = 0;
    var conga = 0;
    var mage = 0;


		async function meanData() {
      try 
      {
          await fetch("http://127.0.0.1:5000/mean")
            .then(response => response.json())
            .then(data => {
              console.log(data.mean);
              mg = data.mean;
              console.log("Inner: "+mg);
              checkCondition();
            })
      } catch(error) {
          console.log(error);
        }
      console.log("Outer: "+mg);
    } 
        meanData()



        async function sdData() {
          try {
          await fetch("http://127.0.0.1:5000/sd")
            .then(response => response.json())
            .then(data => {
              console.log(data.sd);
              sd = data.sd;
              checkCondition();
            })

        } catch(error) {
            console.log(error);
        }
        console.log("outer SD: "+sd);
      }
        sdData()


        async function sdrData() {
          try {
          await fetch("http://127.0.0.1:5000/sdr")
          .then(response => response.json())
          .then(data => {
            console.log("SDR: "+data.dataSDR);
            sdr = data.dataSDR;
          })
        } catch(error) {
          console.log(error)
        }
        console.log("outer SDR: "+sdr);
      }
        sdrData()


        async function gvData() {
          try {
          await fetch("http://127.0.0.1:5000/gv")
            .then(response => response.json())
            .then(data => {
              console.log(data.gv);
              gv = data.gv;
              checkCondition();
            })

        } catch(error) {
            console.log(error);
        }
      }
        gvData()


        async function tirData() {
          try {
          await fetch("http://127.0.0.1:5000/tir_tar_tbr")
            .then(response => response.json())
            .then(data => {
              console.log(data);
              tar = data.tar_percentage;
              tar1 = data.tar1_percentage;
              tar2 = data.tar2_percentage;
              tbr = data.tbr_percentage;
              tbr1 = data.tbr1_percentage;
              tbr2 = data.tbr2_percentage;
              tir = data.tir_percentage;
              checkCondition();
            
            })

        } catch(error) {
          console.log(error);
        }
      }
        tirData()


        async function moddData() {
          try {
          await fetch("http://127.0.0.1:5000/modd")
            .then(response => response.json())
            .then(data => {
              console.log(data);
              modd = data.modd;
              checkCondition();
            })

        } catch(error) {
          console.log(error);
        }
      }
        moddData()


        async function congaData() {
          try {
          await fetch("http://127.0.0.1:5000/conga")
            .then(response => response.json())
            .then(data => {
              console.log(data);
              conga = data.conga;
              checkCondition();
            })

        } catch(error) {
          console.log(error);
        }
      }
        congaData()


        async function mageData() {
          try {
          await fetch("http://127.0.0.1:5000/mage")
            .then(response => response.json())
            .then(data => {
              console.log(data, "HIIImega");
              mage = data
              checkCondition();
            })

        } catch(error) {
          console.log(error);
        }
      }
        mageData()

        function checkCondition() {
        	
          console.log("output: "+mg)
          console.log("output: "+sd)
          console.log("output: "+tar1)
          console.log("output: "+tar2)
          console.log("output: "+tbr1)
          console.log("output: "+tbr2)


          if (mg > 180 && (tar1 > 25 || tar2 > 5) && tir < 70 && sdr > 5 ) { //F1
            document.getElementById("demo").innerHTML = "Case of Hyperglycemia. Adjust the treatment regimen"
          } else if (mg < 180 && (tar1 > 4 || tbr2 > 1) && tir < 70 && sdr > 5 ) { //F2
            document.getElementById("demo").innerHTML = "Case of Hypoglycemia. Adjust the treatment regimen"
          } else if (mg < 180 && (tbr1 > 25 || tar2 > 5) && tir > 70 && sdr < 5 ) {
            document.getElementById("demo").innerHTML = "Case of Hidden Hyperglycemia. Adjust the treatment regimen"
          } else if (mg < 180 && (tbr1 > 4 || tbr2 > 1) && tir > 70 && sdr < 5 ) {
            document.getElementById("demo").innerHTML = "Case of Hidden Hypoglycemia. Adjust the treatment regimen"
          } else if ((tar1 > 25 || tar2 > 5) && (tbr1 > 4 || tbr2 > 1) && tir > 70 && sdr > 5 ) {
            document.getElementById("demo").innerHTML = "Case of Hyper and Hypoglycemia. Adjust the treatment regimen"
          } else if (mg < 180 && (tar1 < 25 || tar2 > 5) && tir > 70 && (tbr1 < 4 || tbr2 < 1) && sdr < 5) {
            document.getElementById("demo").innerHTML = "Normal condition. Continue the treatment regimen"
          }
        }

	</script>

</body>
</html>