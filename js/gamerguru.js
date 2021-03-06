var calendar = new CalHeatMap();
calendar.init({
    data: "data/datas.json",
	start: new Date(2014, 0),
	id : "graph_k",
	domain : "month",
	subDomain : "x_day",
	legend: [60, 70, 80, 90],
	legendLabel: {
			lower: "Releases that scored within {min} {name}",
			inner: "Releases that scored within et {up} {name}",
			upper: "Releases that scored within{max} {name}"
		},
	range : 12,
	cellsize: 15,
	cellpadding: 3,
	cellradius: 5,
	domainGutter: 15,
	weekStartOnMonday: 0,
	
    });