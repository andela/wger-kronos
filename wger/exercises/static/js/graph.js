/* jshint esversion: 6 */


const Compare = (url) => {
  let username = document.getElementById('username').value;
  // set the dimensions and margins of the graph
  const marginTop = 10;
  const marginRight = 30;
  const marginBottom = 20;
  const marginLeft = 50;
  let width = 460 - marginLeft - marginRight;
  let height = 400 - marginTop - marginBottom;
  // append the svg object to the body of the page
  document.getElementById('my_dataviz').innerHTML = '';
  let svg = d3.select('#my_dataviz')
    .append('svg')
    .attr('width', width + marginLeft + marginRight)
    .attr('height', height + marginTop + marginBottom)
    .append('g')
    .attr('transform',
      'translate(' + marginLeft + ',' + marginTop + ')');
  // Parse the Data
  let nal =`${url}${username}`;
  d3.json(nal, data => {
    // List of subgroups = header of the csv files = soil condition here
    let subgroups = ['owner', 'other'];
    // List of groups = species here = value of the first column
    // called group -> I show them on the X axis
    let groups = d3.map(data, d => (d[Object.keys(d)[0]].date)).keys();
    // Add X axis
    let x = d3.scaleBand()
      .domain(groups)
      .range([0, width])
      .padding([0.2]);
    svg.append('g')
      .attr('transform', 'translate(0,' + height + ')')
      .call(d3.axisBottom(x).tickSize(0));
    // Add Y axis
    let y = d3.scaleLinear()
      .domain([0, 180])
      .range([height, 0]);
    svg.append('g')
      .call(d3.axisLeft(y));
    // Another scale for subgroup position?
    let xSubgroup = d3.scaleBand()
      .domain(subgroups)
      .range([0, x.bandwidth()])
      .padding([0.05]);
    // color palette = one color per subgroup
    let color = d3.scaleOrdinal()
      .domain(subgroups)
      .range(['#8d20c0', '#4daf4a']);
    // Show the bars
    svg.append('g')
      .selectAll('g')
      // Enter in data = loop group per group
      .data(data)
      .enter()
      .append('g')
      .attr('transform', d => 'translate(' + x(d[Object.keys(d)[0]].date) + ',0)')
      .selectAll('rect')
      .data(d => subgroups.map(() => ({
        key: Object.keys(d)[0],
        value: d[Object.keys(d)[0]].weight
      })))
      .enter()
      .append('rect')
      .attr('x', d => xSubgroup(d.key))
      .attr('y', d => y(d.value))
      .attr('width', xSubgroup.bandwidth())
      .attr('height', d => height - y(d.value))
      .attr('fill', d => color(d.key));
  });
};
