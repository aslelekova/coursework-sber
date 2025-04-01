import 'package:flutter/material.dart';
import '../moduls/api.dart';

var api = ApiService();

void showThanks(context, List res) {
  showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: Colors.white,
          title: const Text("Результаты", style: TextStyle(color: Color.fromARGB(255, 237, 159, 42), fontWeight: FontWeight.bold, fontSize: 24,), ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Center(
                child: 
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("type: ${res[1]}",
                      style: TextStyle(fontWeight: FontWeight.w600, fontSize: 20),
                    ),
                    SizedBox(height: 10),
                    Text("confidence: ${res[2]}",
                      style: TextStyle(fontWeight: FontWeight.w600, fontSize: 20),
                    ),
                    SizedBox(height: 10),
                    Text("series: ${res[3]}",
                      style: TextStyle(fontWeight: FontWeight.w600, fontSize: 20),
                    ),
                    SizedBox(height: 10),
                    Text("number: ${res[4]}",
                      style: TextStyle(fontWeight: FontWeight.w600, fontSize: 20),
                    ),
                    SizedBox(height: 10),
                    Text("page_number: ${res[5]}",
                      style: TextStyle(fontWeight: FontWeight.w600, fontSize: 20),
                    ),
                  ],
                ),
              ),
            ],
          ),
          actionsAlignment: MainAxisAlignment.center,
          actions: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 15.0),
              child: Row(
                children: [
                  Expanded(
                    child: SizedBox(
                      height: 60,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color.fromARGB(255, 237, 159, 42),
                          shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(12)
                                        )
                        ),
                        onPressed: () {
                          Navigator.pop(context);
                        },
                        child: const Text(
                          "Ок",
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 20,
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        );
      });
}

void showSmthEmpty(context) {
  showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: Colors.white,
          title: const Text("Подсказка", style: TextStyle(color: Color(0xff2b59d3)),),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: const [
              Center(
                child: Text(
                  "Для отправки обращения в поддержку требуется заполнить все поля!",
                  style: TextStyle(color: Color(0xff2b59d3)),
                ),
              ),
            ],
          ),
          actionsAlignment: MainAxisAlignment.center,
          actions: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 15.0),
              child: Row(
                children: [
                  Expanded(
                    child: SizedBox(
                      height: 60,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xff2b59d3),
                          shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(12)
                                        )
                        ),
                        onPressed: () {
                          Navigator.pop(context);
                        },
                        child: const Text(
                          "Ок",
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 20,
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        );
      });
}

// void support(context, TextEditingController nameController,TextEditingController telephoneController, TextEditingController messageController) {
//   bool isNameEmpty = true;
//   bool isPhoneEmpty = true;
//   bool isMessageEmpty = true;
//   var maskForTelephone = MaskTextInputFormatter(
//     mask: '+7 (###) ###-##-##', 
//     filter: { "#": RegExp(r'[0-9]') },
//     type: MaskAutoCompletionType.lazy,
//   );
//   showDialog(context: context, builder: (context)=> AlertDialog(
//     title: const Text('Поддержка'),
//     titleTextStyle: 
//       const TextStyle(
//         fontWeight: FontWeight.bold,
//         color: Colors.black,fontSize: 20),
//     content: SingleChildScrollView(
//       child: Column(
//         mainAxisAlignment: MainAxisAlignment.center,
//         mainAxisSize: MainAxisSize.min,
//         children: [
//           Row(
//             mainAxisAlignment: MainAxisAlignment.start,
//             children:  const [
//               Flexible(child:Text("Для обращения в поддержку заполните поля ниже")),
//             ],
//           ),
//           const SizedBox(height: 10,),
//           TextFormField(
//             onChanged: (value){
//               isNameEmpty = value.isEmpty;
//             },
//             controller: nameController,
//             textCapitalization: TextCapitalization.words,
//             cursorColor: const Color(0xff2b59d3),
//             decoration: const InputDecoration(
//               labelText: "Имя",
//               floatingLabelStyle: TextStyle(color: Color(0xff2b59d3)),
//               focusedBorder: UnderlineInputBorder(
//                 borderSide: BorderSide(
//                   color: Color(0xff2b59d3),
//                 )
//               ),
//             ),
//           ),
//           const SizedBox(height: 10,),
//           TextFormField(
//             onChanged: (value){
//               isPhoneEmpty = value.isEmpty;
//             },
//             controller: telephoneController,
//             cursorColor: const Color(0xff2b59d3),
//             decoration: const InputDecoration(
//               labelText: "Телефон",
//               hintText: "+7 (___) ___-__-__",
//               floatingLabelStyle: TextStyle(color: Color(0xff2b59d3)),
//               focusedBorder: UnderlineInputBorder(
//                 borderSide: BorderSide(
//                   color: Color(0xff2b59d3),
//                 )
//               ),
//             ),
//             inputFormatters: [maskForTelephone],
//             keyboardType: TextInputType.phone,
//           ),
//           const SizedBox(height: 10,),
//           TextFormField(
//             onChanged: (value){
//               isMessageEmpty = value.isEmpty;
//             },
//             controller: messageController,
//             textCapitalization: TextCapitalization.words,
//             cursorColor: const Color(0xff2b59d3),
//             decoration: const InputDecoration(
//               labelText: "Сообщение",
//               floatingLabelStyle: TextStyle(color: Color(0xff2b59d3)),
//               focusedBorder: UnderlineInputBorder(
//                 borderSide: BorderSide(
//                   color: Color(0xff2b59d3),
//                 )
//               ),
//             ),
//           ),
//         ],
//       )
//       ),
//     actions: [
//       TextButton(onPressed: () {
//         Navigator.pop(context, 'Cancel');
//         nameController.clear();
//         telephoneController.clear();
//         messageController.clear();
//         }, child: const Text("Отмена", style: TextStyle(color: Color(0xff2b59d3)))),
//       TextButton(onPressed: () {
//         if ((isNameEmpty == false) && (isMessageEmpty == false) && (isPhoneEmpty == false)) {
//           api.sendForm(nameController.text, telephoneController.text, messageController.text);
//           Navigator.pop(context, 'Ok');
//           showThanks(context);
//           nameController.clear();
//           telephoneController.clear();
//           messageController.clear();
//         } else {
//           showSmthEmpty(context);
//         }
//         } , child: const Text("Отправить", style: TextStyle(color: Color(0xff2b59d3) ),))
//     ],  
//     ));
// }
