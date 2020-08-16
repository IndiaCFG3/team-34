class Event {
  String name;
  String description;
  String location;
  String date;
  String status;

  Event({this.name, this.description, this.location, this.date, this.status});

  Event.fromJson(Map<String, dynamic> json) {
    name = json['name'];
    description = json['description'];
    location = json['area'];
    date = json['scheduledTime'];
    status = json['status'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['name'] = this.name;
    data['description'] = this.description;
    data['scheduledTime'] = this.date;
    data['status'] = this.status;
    data['area'] = this.location;
    return data;
  }
}
