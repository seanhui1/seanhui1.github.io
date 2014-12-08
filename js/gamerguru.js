var calendar = new CalHeatMap();
calendar.init({
    data: "data/datas.json",
	start: new Date(2014, 0),
	id : "graph_k",
	domain : "month",
	subDomain : "x_day",
	range : 12,
	cellsize: 15,
	cellpadding: 3,
	cellradius: 5,
	domainGutter: 15,
	weekStartOnMonday: 0,
	scale: [10, 20, 30, 40],
	onClick: function(date, count) {
		alert("potential game URL here");
	}
    });