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
    const datamg = mg;
    console.log(datamg);
}
