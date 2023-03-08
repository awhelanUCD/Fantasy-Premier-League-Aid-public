/* Javascript file for generating live gameweek table, fixture table and team info */

//--------------------Functions for generating tables------------------------//

// Generates a cell for the rank column
function generateRankCell(cell,rank,change_val){
  text = document.createTextNode(rank+1);
  cell.appendChild(text);

  var img = document.createElement('img');

  // Give different image depending if team has stayed in the same position,
  // fallen position or risen position
  if (change_val=='-')
  {
    img.src='../static/img/greyCircle.svg';
  }
  else if (change_val=='U')
  {
    img.src='../static/img/greenArrow.svg';
  }
  else
  {
    img.src='../static/img/redArrow.svg';
  }

  img.classList.add("imgRankChange")
  cell.appendChild(img)

}

// Generate the cell which gives the player name, this cell also gives the score
// of that players ongoing match and whether they are winning or losing
function generatePlayerNameCell(cell,points,wld){
  let text1=document.createElement('span');
  let text2=document.createTextNode(points);
  cell.appendChild(text1);
  text1.id='score';

  // These classes give the background which the fixture score will be wrapped in
  text1.classList.add("GXDoWd");
  text1.classList.add("Ycf7w");
  text1.classList.add("OGs04e");

  // These give the background a different colour depending on whether the player
  // is winning, losing or drawing
  if (wld=='D'){
    text1.classList.add("teamDrawing");
  }
  else if (wld=='W'){
    text1.classList.add("teamWinning");
  }
  else{
    text1.classList.add("teamLosing");
  }

  text1.appendChild(text2);
}

// Class for generating a live league table
class liveLeagueTable{
  constructor(table,data,columnHeadings,columnNames){
    this.table=table;
    this.data=data;
    this.columnHeadings=columnHeadings;
    this.columnNames=columnNames;
  }

  // Generate the head of the table
  generateTableHead(){
    let thead = this.table.createTHead();
    let row = thead.insertRow();
    for (let key of this.columnHeadings) {
      let th = document.createElement("th");
      th.id=key;
      let text = document.createTextNode(key);
      th.appendChild(text);
      th.classList.add("leagueCol_"+key);
      row.appendChild(th);
    }
  }

  // Generate the body of the table
  generateTableBody(){

    for (let element of this.data)
    {
      let row = this.table.insertRow();
      for (let key of this.columnNames)
      {
        let cell = row.insertCell();
        cell.classList.add("leagueCol_"+key);
        let text = document.createTextNode(element[key]);

        //  Rank and player name column cells are generated in a differnet way
        // to the others, where the text is simply rendered
        if (key=="Rank"){generateRankCell(cell,element[key],element['change_val'])}
        else if (key=='player_name'){
          cell.appendChild(text);
          generatePlayerNameCell(cell,element['points_list'],element['wld_list']);
        }
        else{cell.appendChild(text);}


      }


    }

  }

}

//*** Functions for generating fixtures table ***//

//Generates entry name cell for a row
function generateEntry(row,entryName){
  let cell=row.insertCell();
  let text = document.createTextNode(entryName);
  cell.appendChild(text);
  cell.classList.add('teamEntry');


}

//Genrates buttons which will display team information for each player
function generateButton(row,entryID){

  let cell=row.insertCell();
  let btn = document.createElement("span");
  btn.innerHTML+=`
  <button type="button" class="infoButton" data-toggle="modal" style="border: 0; border-radius: 2em;" data-target="#modal_${entryID}">
  <i class="fa-solid fa-info "></i></button>
  `;
  cell.appendChild(btn);
}

//Generates each players score for row
function generateScore(row,score1,score2){
  let cell=row.insertCell();

  let score_1=document.createElement('span');
  cell.appendChild(score_1);
  let textScore1 = document.createTextNode(String(score1));//+"-"+String(score2));
  score_1.appendChild(textScore1);
  score_1.classList.add('teamScore');

  let score_2=document.createElement('span');
  cell.appendChild(score_2);
  let textScore2 = document.createTextNode(String(score2));//+"-"+String(score2));
  score_2.appendChild(textScore2);
  score_2.classList.add('teamScore');

}

// Class for generating the live fixture scores
class liveFixtureTable{
  constructor(table,data,columnHeadings,columnNames){
    this.table=table;
    this.data=data;
    this.columnHeadings=columnHeadings;
    this.columnNames=columnNames;
  }

  // Generate the head of the table
  generateTableHead(){
    let thead = this.table.createTHead();
    let row = thead.insertRow();
    for (let key of this.columnHeadings) {
      let th = document.createElement("th");
      th.id=key;
      let text = document.createTextNode(key);
      th.appendChild(text);
      //th.classList.add("leagueCol_"+key);
      row.appendChild(th);
    }
  }

  // Generate the body of the table
  generateTableBody(){

    // Create each row and it's constitutive cells
    for (let i = 0; i < this.data.length; i++) {
      let row = this.table.insertRow();
      generateButton(row,this.data[i]['entry_1_entry']);
      generateEntry(row,this.data[i]['entry_1_player_name']);
      generateScore(row,this.data[i]['entry_1_points'],this.data[i]['entry_2_points']);
      generateEntry(row,this.data[i]['entry_2_player_name']);
      generateButton(row,this.data[i]['entry_2_entry']);
    }

  }

}

// Generate the head of the team info table
function  generateTableHead(table,columnHeadings){
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of columnHeadings) {
      let th = document.createElement("th");
      th.id=key;
      let text = document.createTextNode(key);
      th.appendChild(text);
      //th.classList.add("leagueCol_"+key);
      row.appendChild(th);
    }
  }

// Generate the team info table which fills the info modals
function generateTeamInfoTable(table, data, columnHeadings,startIndex) {

  //Player positions and teams are given as integers in the JSOM, these dictionaries
  //give the web app user these valuues in their written form
  var positiondDict = {1: "Goalkeeper", 2: "Defender",3: "Midfielder",4: "Forward" };
  var teamDict = {
    1: "Arsenal", 2: "Aston Villa", 3: "Bournemouth", 4: "Brentford",
    5:"Brighton", 6:"Chelsea" ,7:"Crystal Palace",8: "Everton",
    9: "Fulham",10:"Leicester",11:"Leeds",12: "Liverpool",
    13: "Man City",14: "Man United", 15:"Newcastle",16:"Notts Forest",
    17:"Southampton", 18:"Tottenham",19:"West Ham",20:"Wolves"
  };

  //This variable is used so that players postions aren't repeated one after another
  //in the modal - leading to a cleaner display
  var positionCheck;

  //Loop through the 15 footballers in a users team
  for (let i = 0; i < 15; i++) {

    let element=data[i+startIndex];
    let row = table.insertRow();

    for (let key of columnHeadings) {
      let cell = row.insertCell();
      let text = document.createTextNode(element[key]);

      if (key=="element_type"){
        cell.style.color="#818963";
        if (element[key]==positionCheck)
        {
          text=document.createTextNode("");

        }
        else {
          text=document.createTextNode(positiondDict[element[key]]);
          positionCheck=element[key];
        }
      }

     // The team is given in the form of an image
      if (key=="team"){

        var img = document.createElement('img');
        let num = 15;
        let team_id = element[key].toString();
        img.src=`/static/img/team_images/${team_id}.png`;
        img.classList.add("team_shirt_image");
        //text=document.createTextNode(teamDict[element[key]]);
        cell.appendChild(img)
      }
      else{
        cell.appendChild(text);
      }
    }
  }
}

// Class for generating the modal associated with each team in the fixture table
class modalTeamInfo{
  constructor(teamInfoData,fixtureData,columnHeadings,columnNames){
  this.teamInfoData=teamInfoData;
  this.fixtureData=fixtureData;
  this.columnHeadings=columnHeadings;
  this.columnNames=columnNames;
}

  // Generate the template modal
  generateModalTemplate(){

    let loadingModal = document.getElementById('ModalsDeveloped')
    for (let i = 0; i < this.fixtureData.length; i++) {

      //Html for modal entry 1 (left hand side of fixture table)
      loadingModal.innerHTML +=`
      <div class="modal " id="modal_${this.fixtureData[i]['entry_1_entry']}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog  modal-dialog-centered" role="document">
      <div class="modal-content">
      <div class="modal-header text-center">
      <h5 class="modal-title w-100" id="exampleModalLabel${this.fixtureData[i]['entry_1_entry']}">${this.fixtureData[i]['entry_1_player_name']}</h5>
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
      <span aria-hidden="true">&times;</span>
      </button>
      </div>
      <div class="modal-body">
      <table  id="teamInfo_${this.fixtureData[i]['entry_1_entry']}" class="teamInfoTable" style="background: white">

      </table>
      </div>

      </div>
      </div>
      </div>
      `;

      //Html for modal entry 2 (right hand side of fixture table)
      loadingModal.innerHTML +=`
      <div class="modal " id="modal_${this.fixtureData[i]['entry_2_entry']}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog  modal-dialog-centered" role="document">
      <div class="modal-content">
      <div class="modal-header text-center">
      <h5 class="modal-title w-100" id="modal_title">${this.fixtureData[i]['entry_2_player_name']}</h5>
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
      <span aria-hidden="true">&times;</span>
      </button>
      </div>
      <div class="modal-body">
      <table  id="teamInfo_${this.fixtureData[i]['entry_2_entry']}" class="teamInfoTable" style="background: white">

      </table>
      </div>

      </div>
      </div>
      </div>
      `;
    }

  }

 // Fill the template modal with a table unique for each player
  populateModalTemplate(){

    //Initialise index so that the correct footballer from the JSON will be given for each
    //fpl player
    let indexStart=0;

    for (let i = 0; i < this.fixtureData.length; i++)
    {
      let teamInfoTable=document.getElementById("teamInfo_"+this.fixtureData[i]['entry_1_entry'])
       generateTableHead(teamInfoTable, this.columnHeadings);
      generateTeamInfoTable(teamInfoTable,this.teamInfoData,this.columnNames,indexStart);

      let teamInfoTable2=document.getElementById("teamInfo_"+this.fixtureData[i]['entry_2_entry'])
      generateTableHead(teamInfoTable2, this.columnHeadings);
      generateTeamInfoTable(teamInfoTable2,this.teamInfoData,this.columnNames,indexStart+15);

      indexStart=indexStart+30;
    }
  }

}


//---------------------------------------------------------------------------//

//Generate live table
let table = document.getElementById("liveFPLTable");
let columnHeadings=['Rank','Name','P','W','D','L','Pts','Score'];
let columnNames=['Rank', 'player_name', 'matches_played', 'matches_won', 'matches_drawn', 'matches_lost', 'total','points_for'];

let live_league_table = new liveLeagueTable(table,dataFPL_JSON,columnHeadings,columnNames)
live_league_table.generateTableHead();
live_league_table.generateTableBody();

//Generate Fixture Table
let fixtureTable=document.getElementById('fixtureTable');
let fixtureHeadings=['Team Info','Name','','Name','Team Info']
let fixtureColumns=["entry_1_player_name","entry_1_points","entry_2_player_name","entry_2_points"];

let fixture_table = new liveFixtureTable(fixtureTable,dataFPLFixtures_JSON,fixtureHeadings,fixtureColumns)
fixture_table.generateTableHead();
fixture_table.generateTableBody();


// Create modal and associated table for each fpl player and
let teamInfoColumnHeadings=["Position","Team","Name","Points","Multiplier"]
let teamInfoColumnNames=["element_type","team","web_name","points","multiplier"]

let modal_team_info= new modalTeamInfo(dataFPLTeamInfo_JSON,dataFPLFixtures_JSON,teamInfoColumnHeadings,teamInfoColumnNames)
modal_team_info.generateModalTemplate();
modal_team_info.populateModalTemplate();
