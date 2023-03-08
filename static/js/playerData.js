/* Javascript file for generating checkbox table and player data table */



// The player position and team data are given as integers from the FPL API,
// these dictionaries allow for their conversion into written form
var positionDict = {1: "Gk", 2: "Def",3: "Mid",4: "For" };
var teamDict = {
  1: "Arsenal", 2: "Aston Villa", 3: "Bournemouth", 4: "Brentford",
  5:"Brighton", 6:"Chelsea" ,7:"Crystal Palace",8: "Everton",
  9: "Fulham",10:"Leicester",11:"Leeds",12: "Liverpool",
  13: "Man City",14: "Man United", 15:"Newcastle",16:"Notts Forest",
  17:"Southampton", 18:"Tottenham",19:"West Ham",20:"Wolves"
};

// Class for generating player data table
class playerDataTable{
  constructor(table,tableBody,playerData,columnNames,columnHeadings,columnsToShow){
    this.table=table;
    this.tableBody=tableBody;
    this.playerData=playerData;
    this.columnNames=columnNames;
    this.columnHeadings=columnHeadings;
    this.columnsToShow=columnsToShow;
  }

  // Generate head of table
  generateTableHead(){

    //Initilise table head
    let thead = this.table.createTHead();
    let row = thead.insertRow();

    var count=0;
    //iterate through columns
    for (let key of this.columnNames) {
      let th = document.createElement("th");

      //create unique id for each column head
      var id="col_"+key+"_head"
      th.id=id;

      //Add text to cell
      let text = document.createTextNode(this.columnHeadings[count]);
      th.appendChild(text);

      //This is so only some of the columns are initially shown
      th.style.display="none"
      if (columnsToShow.includes(key)){
        th.style.display="table-cell"

      }

      //ensure thta the fancyTable.js recognises that this data is numerical
      if (count>2){
        th.setAttribute("data-sortas", "numeric");}

        row.appendChild(th);
        count++;
      }

  }

  // Generate table body
  generateTableBody(){

    var count=0;

    //iterate through each row
    for (let element of this.playerData) {
      let row = this.tableBody.insertRow();
      //iterate through each column
      for (let key of this.columnNames) {

       //intitlise cell
        let cell = row.insertCell();
        var cell_class="col_"+key
        cell.classList.add(cell_class);
        let text = document.createTextNode(element[key]);

        //Ensure that the written form of the players position is given
        if (key=="element_type")
        {
          text=document.createTextNode(positionDict[element[key]]);
        }

        //Create element for the team column
        if (key=="team"){

          var name = document.createElement('span');
          name.innerHTML=teamDict[element[key]];
          name.classList.add("player_team_name")
          cell.appendChild(name)

          var div=document.createElement('div');
          div.classList.add("team_image_div");
          var img = document.createElement('img');
          let num = 15;
          let team_id = element[key].toString();
          img.src=`/static/img/team_images/${team_id}.png`;
          img.classList.add("team_shirt_image2");
          div.appendChild(img)
          //text=document.createTextNode(teamDict[element[key]]);
          cell.appendChild(div)

        }
        else{
          //Set all cells to be hidden
          cell.style.display="none";

          //Set cells belonging to selected columns to be shown
          if (this.columnsToShow.includes(key)){
            cell.style.display="table-cell";

          }
          cell.appendChild(text);}
        }

     }


  }
}


// This functon ensures that each column is shown/hidden when interacted with
// on the checkbox table

function hide_show_table(col_name)
{
  var checkbox_val=document.getElementById(col_name).value;
  console.log(checkbox_val)
  if(checkbox_val=="show")
  {
    var all_col=document.getElementsByClassName(col_name);

    for(var i=0;i<all_col.length;i++)
    {
      all_col[i].style.display="none";
    }
    document.getElementById(col_name+"_head").style.display="none";
    document.getElementById(col_name).value="hide";
  }

  else
  {
    var all_col=document.getElementsByClassName(col_name);

    for(var i=0;i<all_col.length;i++)
    {
      all_col[i].style.display="table-cell";
    }
    document.getElementById(col_name+"_head").style.display="table-cell";
    document.getElementById(col_name).value="show";
  }
}

// Generate head rows for the checkbox table
function generateHeadRow(table,heading){
    let headRow = table.insertRow();
    let headCell = headRow.insertCell();
    headCell.classList.add("checked_table_head");
    let headText = document.createTextNode(heading);
    headCell.appendChild(headText );

  }


// Function for creating cells in the checkbox table
function createCheckboxTableCell(row,key,columnsToShow,rowHeading){

  let cell = row.insertCell();

  var input = document.createElement('input');
  input.setAttribute("type","checkbox")
  input.setAttribute("style","height: 11px; width: 11px;" )
  var id="col_"+key
  input.setAttribute("id",id)
  input.setAttribute("value","hide")

  input.setAttribute("onchange","hide_show_table(this.id);")

  // Certain columns are shown by default
  if (columnsToShow.includes(key)){
    input.setAttribute("value","show")
    input.setAttribute("checked","")
  }

  cell.appendChild(input);

  let text = document.createTextNode(" "+rowHeading);
  cell.appendChild(text);

}

// Class for generating checkbox table, this table allows users to dynamically
// add or remove columns
class checkboxTable{
  constructor(table,columnsToShow,col_number){
    this.table=table;
    this.columnsToShow=columnsToShow;
    this.col_number=col_number;
  }

  fillCheckboxTable(rowNames,rowHeadings,heading){

    // Generate the head row
    generateHeadRow(this.table,heading);

    let row = this.table.insertRow();
    var count=0;
    for (let key of rowNames)
    {

     // generate constitutive cells
      createCheckboxTableCell(row,key,this.columnsToShow,rowHeadings[count])
      count++;

      // After a defined number, create a new row
      if (count/this.col_number==1){
        row=table.insertRow();
      }
    }

  }

}

// Column names and associated headings given as dictionaries with 4 headings: fundamental, basic,
// advanced and per90

let columnNames={
  "fundamental":['team','web_name'],
  "basic":['element_type',
  'assists','goals_scored','clean_sheets','goals_conceded',
  'total_points','points_per_game', 'starts'],
  "advanced":['expected_assists','expected_goals',
  'expected_goals_conceded', 'expected_goal_involvements'],
  "per_90":['expected_assists_per_90','expected_goals_per_90',
  'expected_goals_conceded_per_90','expected_goal_involvements_per_90',
  'starts_per_90']
}

let columnHeadings={"fundamental":['Team','Name',],
"basic":[ 'Postion',
'Assists','Goals Scored','Clean Sheets','Goals Conceded',
'Points','Points PG','Starts'],
"advanced":[ 'Expected Assists', 'Expected Goals',
'Expected Goals Conc', 'Expected Goal Inv',],
"per_90":[ 'Expected Assists p90','Expected Goals p90',
'Expected Goals Conc p90','Expected Goal Inv p90',
'Starts p90']
}

// Create lists contaings all the column names and headings for generating the
// player data table
let allColumnNames=columnNames["fundamental"].concat(columnNames["basic"],columnNames["advanced"],columnNames["per_90"])
let allColumnHeadings=columnHeadings["fundamental"].concat(columnHeadings["basic"],columnHeadings["advanced"],columnHeadings["per_90"])

// These columns will be intially shown to the user
let columnsToShow=['team','web_name','element_type', 'assists','goals_scored','total_points']

// Create player data table
let table = document.getElementById("playerDataTable");
let tableBody = document.getElementById("liveFPLTableBody");
player_data_table=new playerDataTable(table,tableBody, dataFPL_JSON,allColumnNames,allColumnHeadings,columnsToShow)
player_data_table.generateTableHead();
player_data_table.generateTableBody();

// Create checkbox table
table = document.getElementById("checkbox_table");
let checkbox_table = new checkboxTable(table,columnsToShow,4)
checkbox_table.fillCheckboxTable(columnNames["basic"],columnHeadings["basic"],"Basic")
checkbox_table.fillCheckboxTable(columnNames["advanced"],columnHeadings["advanced"],"Advanced")
checkbox_table.fillCheckboxTable(columnNames["per_90"],columnHeadings["per_90"],"Per 90 Minutes")
