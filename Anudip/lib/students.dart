import 'package:flutter/material.dart';

class Students extends StatelessWidget {
  const Students({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      child: ListView(
        children: [
          Card(
            margin: EdgeInsets.all(20),
            child: 
            Row(
              children: [
                 Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(10.0),
                      child: Text("Name : Khushi Jashnani"),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(10.0),
                      child: Text("Phone : 9729388383"),
                    ),
                  ],
                ),
             ],
            )
           
          ),
          Card(
            margin: EdgeInsets.all(20),
            child: 
            Row(
              children: [
                 Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(10.0),
                      child: Text("Name : Riddhi Gupta"),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(10.0),
                      child: Text("Phone : 97293488383"),
                    ),
                  ],
                ),
             ],
            )
           
          ),
          Card(
            margin: EdgeInsets.all(20),
            child: 
            Row(
              children: [
                 Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(10.0),
                      child: Text("Name : Jai Kathuria"),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(10.0),
                      child: Text("Phone : 9729342423"),
                    ),
                  ],
                ),
             ],
            )
           
          )
        ],
      )
    );
  }
}