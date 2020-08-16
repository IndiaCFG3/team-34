import 'dart:convert';

import 'package:Anudip/models/events.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class CreateEvent extends StatefulWidget {
  Event e;
  CreateEvent({Key key, this.e}) : super(key: key);

  @override
  _CreateEventState createState() => _CreateEventState();
}

class _CreateEventState extends State<CreateEvent> {
  TextEditingController description;
  TextEditingController name;
  TextEditingController location;
  String statusValue = 'Not Completed';
  DateTime date;
  // TextEditingController description;
  // TextEditingController description;
  final eventkey = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();
    date = DateTime.now();
    name = TextEditingController();
    description = TextEditingController();
    location = TextEditingController();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        padding: EdgeInsets.fromLTRB(20, 20, 20, 20),
        child: ListView(
          children: [
            Container(
                height: 50,
                child: Text(
                  "Enter event details :",
                  style: TextStyle(fontSize: 30),
                )),
            Form(
              key: eventkey,
              child: Column(
                children: [
                  TextFormField(
                    controller: name,
                    decoration: InputDecoration(
                        //border: InputBorder.none,
                        labelText: 'Name',
                        hintText: widget.e != null ? widget.e.name : "",
                        hintStyle: TextStyle(color: Colors.grey)),
                  ),
                  TextFormField(
                    controller: description,
                    maxLines: 3,
                    decoration: InputDecoration(
                        //border: InputBorder.none,
                        labelText: "Description",
                        hintText: widget.e != null ? widget.e.description : "",
                        hintStyle: TextStyle(color: Colors.grey)),
                  ),
                  TextFormField(
                    controller: location,
                    decoration: InputDecoration(
                        //border: InputBorder.none,
                        labelText: "Location",
                        hintText: widget.e != null ? widget.e.location : "",
                        hintStyle: TextStyle(color: Colors.grey)),
                  ),
                  Container(
                      child: FlatButton(
                    child: Text("Select Date"),
                    onPressed: () async {
                      DateTime d = await showDatePicker(
                          context: context,
                          initialDate: DateTime.now(),
                          firstDate: DateTime.now(),
                          lastDate: DateTime(2021));
                      setState(() {
                        date = d;
                      });
                    },
                  )),
                  Container(
                      child: Text(date.day.toString() +
                          "/" +
                          date.month.toString() +
                          "/" +
                          date.year.toString())),
                  // InputDatePickerFormField(
                  //     fieldLabelText: "Date",
                  //     firstDate: DateTime.now(),
                  //     lastDate: DateTime(2021)),
                  DropdownButtonFormField(
                    items: <String>['Not Completed', 'Completed']
                        .map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value,
                            style: TextStyle(
                              color: Colors.blue,
                            )),
                      );
                    }).toList(),
                    iconSize: 20,
                    elevation: 16,
                    icon: Icon(Icons.arrow_drop_down),
                    onChanged: (newValue) {
                      setState(() {
                        statusValue = newValue;
                        print(statusValue);
                      });
                    },
                    value: widget.e != null ? widget.e.status : statusValue,
                  ),
                ],
              ),
            ),
            RaisedButton(
              onPressed: () {
                submit();
              },
              color: Colors.blue,
              child: Text("Submit"),
            ),
          ],
        ));
  }

  submit() async {
    SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
    if (name.text != "" &&
        description.text != "" &&
        location.text != "" &&
        date.day != null) {
      Event e = Event(
          name: name.text,
          description: description.text,
          location: location.text,
          date: date.year.toString() +
              "-" +
              date.month.toString() +
              "-" +
              date.day.toString(),
          status: statusValue);

      print(json.encode(e));
      var response =
          await http.post('https://project-umeed.herokuapp.com/app/mob/event/',
              headers: {
                "Authorization":
                    "Token " + sharedPreferences.getString('token'),
                'Content-Type': 'application/json'
              },
              body: json.encode(e));

      if (response.statusCode == 200) {
        print("success");
      } else {
        print("fail");
      }
      
    }
  }
}
