var Person = function (x){
  if(x){
    this.fullname = x;
  }
};

Person.prototype.whatIsMyFullname = function(){
return this.fullname;
};

Person.prototype.fullname = 'fucking enter the name, dude';

var yo = new Person('yo');
var fuck = new Person('fck');
var hey = new Person();

yo.whatIsMyFullname();
fuck.whatIsMyFullname();

hey.whatIsMyFullname();

var foo = new Array();

Array.prototype.word = 'aa';

console.log(foo);

var test = function(){
  foo = 2;

};

console.log(foo.constructor.prototype.word);
