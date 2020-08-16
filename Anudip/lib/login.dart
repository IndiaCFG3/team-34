import 'dart:convert';

import 'package:Anudip/home.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class LoginPage extends StatefulWidget {
  LoginPage({Key key}) : super(key: key);

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController phoneController;
  TextEditingController passController;
  bool passvis = true;
  final _loginFormKey = GlobalKey<FormState>();
  final _scaffoldKey1 = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    phoneController = TextEditingController();
    passController = TextEditingController();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        margin: EdgeInsets.fromLTRB(20, 0, 20, 0),
        child: Center(
            child: Form(
          key: _loginFormKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Container(
                child: Text(
                  "LOG IN",
                  style: TextStyle(fontSize: 30, color: Colors.cyan),
                ),
              ),
              SizedBox(
                height: 20,
              ),
              Container(
                padding: EdgeInsets.all(10),
                decoration: BoxDecoration(
                    border:
                        Border(bottom: BorderSide(color: Colors.grey[200]))),
                child: TextFormField(
                  keyboardType: TextInputType.phone,
                  validator: (value) {
                    if (value.isEmpty) {
                      return 'Please enter your phone Number';
                    }
                    if (!RegExp(r"^(?=.*\d)[\d]{10}$")
                        .hasMatch(phoneController.text)) {
                      return "Only 10 digits allowed\nDon't Include Country Code";
                    }
                    return null;
                  },
                  controller: phoneController,
                  decoration: InputDecoration(
                      border: InputBorder.none,
                      hintText: "Phone Number",
                      hintStyle: TextStyle(color: Colors.grey)),
                ),
              ),
              Container(
                  padding: EdgeInsets.all(10),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Expanded(
                        child: TextFormField(
                          obscureText: passvis,
                          validator: (value) {
                            if (value.isEmpty) {
                              return 'Please enter a Password';
                            }
                            // if (!RegExp(
                            //         r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
                            //     .hasMatch(passController.text)) {
                            //   return "Please include atleast 1 lowercase, 1 uppercase,\n1 digit and 1 special character";
                            // }
                            return null;
                          },
                          controller: passController,
                          decoration: InputDecoration(
                              border: InputBorder.none,
                              hintText: "Password",
                              hintStyle: TextStyle(color: Colors.grey)),
                        ),
                      ),
                      InkWell(
                          onTap: () {
                            setState(() {
                              passvis = !passvis;
                            });
                          },
                          child: Icon(
                            passvis ? Icons.visibility : Icons.visibility_off,
                            color: Colors.cyan[700],
                          ))
                    ],
                  )),
              GestureDetector(
                onTap: () {
                  // if (passController.text.isEmpty ||
                  //     phoneController.text.isEmpty) {
                  //   _scaffoldKey1.currentState.showSnackBar(SnackBar(
                  //     content: Text('Fields Cannot be Empty'),
                  //     duration: Duration(seconds: 2),
                  //     backgroundColor: Colors.cyan,
                  //   ));
                  // }
                  // if (!RegExp(r"^(?=.*\d)[\d]{10}$")
                  //     .hasMatch(phoneController.text)) {
                  //   _scaffoldKey1.currentState.showSnackBar(SnackBar(
                  //     content: Text(
                  //         'Enter a Valid Phone Number\nDo not include Country Code i.e +91'),
                  //     duration: Duration(seconds: 2),
                  //     backgroundColor: Colors.cyan,
                  //   ));
                  // }
                  if (_loginFormKey.currentState.validate()) {
                    login(phoneController.text, passController.text);
                  }
                },
                child: Container(
                  height: 50,
                  margin: EdgeInsets.symmetric(horizontal: 100),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(50),
                    color: Colors.cyan,
                  ),
                  child: Center(
                    child: Text("Login Now !",
                        style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 17)),
                  ),
                ),
              )
            ],
          ),
        )));
  }

  login(phone, pass) async {
    var data = {'phone_no': phone, 'password': pass};
    var jsonData = null;
    SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
    var response = await http
        .post('https://project-umeed.herokuapp.com/app/mob/login/', body: data);
    if (response.statusCode == 200) {
      jsonData = json.decode(response.body);
      setState(() {
        print("id="+jsonData['User']['id'].toString());
        sharedPreferences.setString("id", jsonData['User']['id'].toString());
        sharedPreferences.setString("token", jsonData['User']['token']);
      });
      Navigator.push(
          context,
          MaterialPageRoute(builder: (BuildContext context) => HomePage()),
          );
    } else {
      print(response.body);
    }
  }
}
