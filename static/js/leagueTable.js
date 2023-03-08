/* Javascript file for generating league table */


// Gives colour scale for global percentile column
f=chroma.scale(['blue', 'red']);


// Function to generate cell for global percentile column
function generatePercentileCell(cell,percentile)
{
  let text = document.createTextNode(percentile);
  color=f(percentile/100)
  cell.setAttribute("style",`color: ${color}; font-weight: 1000;`)
  cell.appendChild(text)
}

// Function to generate cell for head-to-head form column
function generateFormCell(cell,form)
{
  for (let i = 0; i < form.length; i++)
   {

    cell.id='formIcons';
    var img = document.createElement('img');

    // Give different image depending on fixture result
    if (form[i]=='W')
    {
      img.src="../static/img/W.svg";
    }
    else if (form[i]=='L')
    {
      img.src="../static/img/L.svg";
    }
    else
    {
      img.src="../static/img/D.svg";
    }
    cell.appendChild(img)
  }
}

// Class for generating league table
class leagueTable
{
  constructor(table,data,columnHeadings,columnNames)
  {
    this.table=table;
    this.data=data;
    this.columnHeadings=columnHeadings;
    this.columnNames=columnNames;
  }

  // Generate the table head
  generateTableHead()
  {
    let thead = this.table.createTHead();
    let row = thead.insertRow();

    for (let key of this.columnHeadings)
    {
      let th = document.createElement("th");
      th.id=key;
      let text = document.createTextNode(key);
      th.appendChild(text);

    // when there are spaces in the head names js gives an error
    // try/catch works for now but is something to improve on
      try{th.classList.add("leagueColHead_"+key);}
      catch(error){}
      try{th.id="leagueColHead_id_"+key;}
      catch(error){}
      row.appendChild(th);
    }
  }

  // Generate the table body
  generateTableBody()
  {

    for (let element of this.data)
    {
      // generate new row
      let row = this.table.insertRow();

      // Generate each column
      for (let key of this.columnNames)
      {

        let cell = row.insertCell();
        cell.classList.add("leagueCol_"+key);

        // Form and percentile columns are displayed in a different way to the
        // others, where only the text needs to be rendered
        if (key =='form')
        {
          let form=element[key];
          generateFormCell(cell,form);
        }

        else if (key=='percentile')
        {
          let percentile=Math.trunc(element[key])
          generatePercentileCell(cell,percentile);
        }
        else
        {
          let text = document.createTextNode(element[key]);
          cell.appendChild(text);
        }
      }
    }

  }

}

// Render league table in HTML
let table = document.getElementById("FPLleagueTable");
league_table= new leagueTable(table,dataFPL_JSON,columnHeadings,columnNames)
league_table.generateTableHead();
league_table.generateTableBody();
