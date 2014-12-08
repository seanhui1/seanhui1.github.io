var calendar = new CalHeatMap();
calendar
	data: "datas.json",
	start: new Date(2014, 1),
	id : "graph_k",
	domain : "month",
	subDomain : "x_day",
	range : 12,
	cellsize: 15,
	cellpadding: 3,
	cellradius: 5,
	domainGutter: 15,
	weekStartOnMonday: 0,
	scale: [10, 20, 80, 100]
});