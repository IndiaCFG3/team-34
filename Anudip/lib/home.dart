import 'package:Anudip/createEvent.dart';
import 'package:Anudip/events.dart';
import 'package:Anudip/login.dart';
import 'package:Anudip/students.dart';
import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  HomePage({Key key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int state;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    state = 0;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Home Page"),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            DrawerHeader(
              child: Text('Drawer Header'),
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
            ),
            ListTile(
              title: Text('Your Events'),
              onTap: () {
                setState(() {
                  state = 0;
                });
                Navigator.pop(context);
              },
            ),
            ListTile(
              title: Text('Create an Event'),
              onTap: () {
                setState(() {
                  state = 1;
                });
                Navigator.pop(context);
              },
            ),
             ListTile(
              title: Text('Students'),
              onTap: () {
                setState(() {
                  state = 2;
                });
                Navigator.pop(context);
              },
            ),
            ListTile(
              title: Text('Log Out'),
              onTap: () {
                
                Navigator.push(context, MaterialPageRoute(builder: (context) => LoginPage(),));
              },
            ),
          ],
        ),
      ),
      body: getPage(),
    );
  }

  getPage() {
    switch (state) {
      case 0:
        return Events();
        break;
      case 1:
        return CreateEvent();
        break;
      case 2:
        return Students();
        break;
      default:
        return Events();
    }
  }
}
