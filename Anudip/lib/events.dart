import 'dart:convert';
import 'package:Anudip/models/events.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class Events extends StatefulWidget {
  Events({Key key}) : super(key: key);

  @override
  _EventsState createState() => _EventsState();
}

class _EventsState extends State<Events> {
  ScrollController scrollController;
  List<Event> events = [];

  // getevents() async {
  //   SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
  //   String api = 'https://project-umeed.herokuapp.com/app/mob/event/' +
  //       sharedPreferences.getString('id').toString() +
  //       '/';
  //   final response = await http.get(api);
  //   print(json.decode(response.body)['Events']);
  //   return json.decode(response.body)['Events'];
  // }

  getEv() async {
    SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
    String api = 'https://project-umeed.herokuapp.com/app/mob/event/' +
        sharedPreferences.getString('id').toString() +
        '/';
    final response = await http.get(api);
    print(json.decode(response.body)['Events']);
    var ev = json.decode(response.body)['Events'];
    //List<Event> e = [];
    setState(() {
      for (var item in ev) {
        print(Event.fromJson(item));
        events.add(Event.fromJson(item));
      }
    });
    print(events);
    //return e;
  }

  @override
  void initState() {
    super.initState();
    print("nkjdn");
    events = [];
    scrollController = ScrollController();
    getEv();
    print("events");
    print(events);
    print("Sdfsfs");
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        child:
            // FutureBuilder<EventListModel>(
            //     future: events,
            //     builder: (context, snapshot) {
            //       if (snapshot.hasData) {
            //         if (snapshot.data.eventList != null) {
            //           if (snapshot.data.eventList.length > 0) {
            //             return
            ListView.builder(
                controller: scrollController,
                itemCount: events.length, //snapshot.data.eventList.length,
                itemBuilder: (BuildContext context, int index) {
                  return Card(
                      margin: EdgeInsets.all(15),
                      elevation: 10,
                      borderOnForeground: true,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Padding(
                                padding:
                                    const EdgeInsets.fromLTRB(15.0, 8, 15, 8),
                                child:
                                    Text("EVENT No. " + (index + 1).toString()),
                              ),
                              Padding(
                                padding:
                                    const EdgeInsets.fromLTRB(15.0, 8, 15, 8),
                                child: RaisedButton(
                                  onPressed: () {
                                    
                                  },
                                  child: Text("Edit"),
                                ),
                              )
                            ],
                          ),
                          Padding(
                            padding: const EdgeInsets.fromLTRB(20, 5, 10, 5),
                            child: Text("Name: " + events[index].name),
                          ),
                          Padding(
                            padding: const EdgeInsets.fromLTRB(20, 5, 10, 5),
                            child: Text(
                                "Description: " + events[index].description),
                          ),
                          Padding(
                            padding: const EdgeInsets.fromLTRB(20, 5, 10, 5),
                            child: Text("Date: " + events[index].date),
                          ),
                          Padding(
                            padding: const EdgeInsets.fromLTRB(20, 5, 10, 20),
                            child: Text("Status: " + events[index].status),
                          ),
                        ],
                      ));
                })
        //     }
        //   }
        // }
        );
  }
}
