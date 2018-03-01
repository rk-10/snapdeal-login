import requests
import getpass

class Snapdeal:

     def __init__(self):
         self.mobile = input('Enter your mobile number : ')
         self.password = getpass.getpass('Enter your password')
         self.session = requests.session()
         self.headers = {}

     def lets_login(self):
         login_json = {}
         url = "https://mobileapi.snapdeal.com/service/user/login/v2/loginWithMobile"

         #Version of app used
         self.headers['v'] = '6.3.6'
         #OperatingSystem used
         self.headers['os'] = 'android'
         #Content encode format
         self.headers['Content-Type'] = 'application/json; charset=utf-8'
         #Host
         self.headers['Host'] = 'mobileapi.snapdeal.com'
         login_json['mobileNumber'] = self.mobile
         login_json['password'] = self.password
         login_json['apiKey'] = 'snapdeal'

         self._login = self.session.post(url, json=login_json, headers=self.headers)

     def add_item_to_Cart(self):
         cart_json = {}
         url = 'https://mobileapi.snapdeal.com/service/nativeCart/v2/insertItemToCart'

         #TokenNumber issued after successfully logging in
         self.headers['Login-Token'] = self._login.headers['Login-Token']
         cart_json['loginToken'] = self.headers['Login-Token']

         #Details of Item being added to cart
         cart_json['items'] = [{"catalogId": 621001398240, "supc": "SDL044460243", "vendorCode": "S333f8",
                                       "quantity": 1}]

         addtocart = self.session.post(url, headers = self.headers, json=cart_json)

         string = ''.join(addtocart.json()['messages'])
         if 'Already Exists' in string:
             raise Exception('This product ' + string + ' in your cart, please remove it and then try again!')


     def lets_logout(self):
         url = 'https://mobileapi.snapdeal.com/service/signout'
         self.session.post(url, headers=self.headers, json={"loginToken":self.headers['Login-Token']})

if __name__ == '__main__':
    letsgo = Snapdeal()
    letsgo.lets_login()
    letsgo.add_item_to_Cart()
    letsgo.lets_logout()
