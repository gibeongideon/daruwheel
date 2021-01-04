import Vue from 'vue'
import swal from 'sweetalert2'
var autobahn = require('autobahn');
import css from './app.css';

// user updates queue
var queued_token_update = undefined
var queued_win_update = undefined
function process_queued_updates() {
    if (queued_token_update) {
        process_update(queued_token_update)
    }
    if (queued_win_update) {
        process_update(queued_win_update)
    }
}
function process_update(el) {
    if (el.type == 'tokens_count') {
        // clear queue
        queued_token_update = undefined
        // update value
        app.token_count = el.value
    } else if (el.type == 'roulette_win') {
        // clear queue
        queued_win_update = undefined
        // show fancy popup
        swal({
          title: 'Success',
          text: 'You win ' + el.value + ' tokens!',
          type: 'success',
          confirmButtonText: 'Cool'
        })
    }
}

/** Autobahn.JS **/
var connection = new autobahn.Connection({url: 'ws://crossbar:8080/ws', realm: 'realm1'});
var sess = null;

connection.onopen = function (session) {

    sess = session

   // 1) subscribe to a topic
   function onevent(args) {
      console.log("Event:", args[0]);
   }
   session.subscribe('com.myapp.hello', onevent);

   // 2) publish an event
   session.publish('com.myapp.hello', ['Hello, world!']);

   // 3) register a procedure for remoting
   function add2(args) {
      return args[0] + args[1];
   }
   session.register('com.myapp.add2', add2);

   // 4) call a remote procedure
   session.call('com.myapp.add2', [2, 3]).then(
      function (res) {
         console.log("Result:", res);
      }
   );

    function roulette_draw(args) {
        var number = args[0];

        console.log("Got com.casino.roulette_draw:", number);
        function endCallback(rotation) {
            oldrotation = rotation
            // update latest numbers
            var tmp = app.latest_draws;
            tmp.unshift(number);
            app.latest_draws = tmp.slice(0, 10)
            process_queued_updates()
            // reset current bets
            app.current_bets.green = []
            app.current_bets.red = []
            app.current_bets.black = []
        }
        spinTo(number, endCallback);
    }

    session.subscribe('com.casino.roulette_draw', roulette_draw);
};

connection.open();

/** VueJS **/
var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    f2msg: '',
    f2msgs: [],
    deposit_currency: '',
    deposit_amount: '',
    deposit_stripeToken: '',
    deposit_stripeEmail: '',
    latest_draws: (typeof vue_latest_draws === 'undefined') ? [] : vue_latest_draws,
    latest_messages: (typeof vue_latest_messages === 'undefined') ? [] : vue_latest_messages,
    token_count: (typeof vue_token_count === 'undefined') ? 0 : vue_token_count,
    user_id: (typeof vue_user_id === 'undefined') ? undefined : vue_user_id,
    username: (typeof vue_username === 'undefined') ? undefined : vue_username,
    bet_amount: 1,
    shoutbox_message: '',
    current_bets: (typeof vue_current_bets === 'undefined') ?
        {
            'green': [], 'red': [], 'black': []
        } : vue_current_bets,
  },
  computed: {
    // a computed getter
    deposit_amount_cents: function () {
      // `this` points to the vm instance
      if (this.deposit_amount) {
          return this.deposit_amount * 100
      }
      return 0
    }
},
  methods: {
    deposit_pay: function (event) {
        stripe_handler.open({
            amount: 100 * this.amount,
            name: 'Casino',
            description: 'Packet of tokens',
        });
    },
    roulette_number_is_green: function (number) {
        if (number == 0) {
            return true
        }
        return false
    },
    roulette_number_is_black: function (number) {
        if (((1 <= number) && (number <= 10)) || ((19 <= number) && (number <= 28))) {
            if (number % 2 == 0)
                return true
            return false
        }
        if (((11 <= number) && (number <= 18)) || ((29 <= number) && (number <= 36))) {
            if (number % 2 == 0)
                return false
            return true
        }
        return false
    },
    roulette_number_is_red: function (number) {
        if (this.roulette_number_is_green(number) || this.roulette_number_is_black(number)) {
            return false
        }
        return true
    },
    subscribe_updates: function(user_id) {
        function user_update(args) {
            console.log('Got user update:', args)
            var received_data = args[0]
            for (var i = 0; i < received_data.length; i++) {
                var el = received_data[i]
                if (el.type == 'tokens_count' && el.delayed == true) {
                    queued_token_update = el
                } else if (el.type == 'roulette_win' && el.delayed == true) {
                    queued_win_update = el
                } else {
                    process_update(el)
                }
            }
        }
        sess.subscribe('com.casino.updates.user' + user_id, user_update)
        console.log('com.casino.updates.user subscribed')
    },
    bet: function(color) {
        if (this.user_id == undefined) {
            swal({
              title: 'Error',
              text: 'You have to be logged!',
              type: 'error',
              confirmButtonText: 'Ok'
            })
        } else {
            sess.call('com.casino.wamp_bet', [
                this.user_id,
                this.bet_amount,
                color,
            ]).then(function (result) {
                if (result.type == 'not_enough_tokens') {
                    swal({
                      title: 'Error',
                      text: 'You do not have enough tokens!',
                      type: 'error',
                      confirmButtonText: 'Ok'
                    })
                }
            });
        }
    },
    send_message: function() {
        if (this.user_id == undefined) {
            swal({
              title: 'Error',
              text: 'You have to be logged!',
              type: 'error',
              confirmButtonText: 'Ok'
            })
        } else {
            sess.call('com.casino.send_message_wamp', [
                this.user_id,
                this.shoutbox_message
            ]).then(function (result) {
                console.log('Call to com.casino.send_message_wamp successful:', result);
            });
        }
    },
    subscribe_shoutbox: function() {
        function shoutbox_update(args) {
            console.log('Got shoutbox update:', args)
            var received_data = args[0]
            for (var i = 0; i < received_data.length; i++) {
                var el = received_data[i]
                if (el.type == 'message') {
                    app.latest_messages.unshift(el.value)
                }
            }
        }
        sess.subscribe('com.casino.shoutbox', shoutbox_update)
        console.log('com.casino.shoutbox subscribed')
    },
    subscribe_current_bets: function() {
        function current_bets_update(args) {
            console.log('Got current bets update:', args)
            var received_data = args[0]
            for (var i = 0; i < received_data.length; i++) {
                var el = received_data[i]
                if (el.type == 'bet' && el.color) {
                    app.current_bets[el.color].unshift(el.value)
                }
            }
        }
        sess.subscribe('com.casino.current_bets', current_bets_update)
        console.log('com.casino.current_bets subscribed')
    },
  }
})
// bind app to window
window.app = app
Vue.config.devtools = true;

/** Stripe **/
var stripe_handler = StripeCheckout.configure({
    key: 'pk_test_Iawjq0y9zDz43I76IOYeCiKX',
    image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
    token: function(token) {
        app.deposit_stripeToken = token.id;
        app.deposit_stripeEmail = token.email;
        // submit form after DOM is updated
        Vue.nextTick(function () {
            app.$refs.deposit_form.submit();
        });
    }
});

window.addEventListener('popstate', function(event) {
    stripe_handler.close();
}, false);

/** D3 **/
var d3 = require("d3");

var data = [
    {"label":"0", "value": 0},
    {"label":"32", "value": 32},
    {"label":"15", "value": 15},
    {"label":"19", "value": 19},
    {"label":"4", "value": 4},
    {"label":"21", "value": 21},
    {"label":"2", "value": 2},
    {"label":"25", "value": 25},
    {"label":"17", "value": 17},
    {"label":"34", "value": 34},
    {"label":"6", "value": 6},
    {"label":"27", "value": 27},
    {"label":"13", "value": 13},
    {"label":"36", "value": 36},
    {"label":"11", "value": 11},
    {"label":"30", "value": 30},
    {"label":"8", "value": 8},
    {"label":"23", "value": 23},
    {"label":"10", "value": 10},
    {"label":"5", "value": 5},
    {"label":"24", "value": 24},
    {"label":"16", "value": 16},
    {"label":"33", "value": 33},
    {"label":"1", "value": 1},
    {"label":"20", "value": 20},
    {"label":"14", "value": 14},
    {"label":"31", "value": 31},
    {"label":"9", "value": 9},
    {"label":"22", "value": 22},
    {"label":"18", "value": 18},
    {"label":"29", "value": 29},
    {"label":"7", "value": 7},
    {"label":"28", "value": 28},
    {"label":"12", "value": 12},
    {"label":"35", "value": 35},
    {"label":"3", "value": 3},
    {"label":"26", "value": 26}
];

// latest draw number -> needed for calculating base wheel rotation
var latest_num = app.latest_draws[0] || 0

var padding = {top:20, right:40, bottom:0, left:0},
    w = 500 - padding.left - padding.right,
    h = 500 - padding.top  - padding.bottom,
    r = Math.min(w, h)/2,
    rotation = 0,
    oldrotation = getRotationForNumber(latest_num),
    picked = 100000,
    color = function(d) {
        if (d == 0) {
            return "green";
        } else if (d % 2 == 0) {
            return "black";
        }
        return "red";
    }

var svg = d3.select('#roulette')
    .append("svg")
    .data([data])
    .attr("width",  w + padding.left + padding.right)
    .attr("height", h + padding.top + padding.bottom);

var container = svg.append("g")
    .attr("class", "chartholder")
    .attr("transform", "translate(" + (w/2 + padding.left) + "," + (h/2 + padding.top) + ")");

var vis = container
    .append("g")

// match rotation with last number
vis.attr("transform", function(d) {
    return "rotate(" + getRotationForNumber(latest_num) + ")";
});

var pie = d3.pie().sort(null).value(function(d){return 1;});

// declare an arc generator function
var arc = d3.arc()
    .innerRadius(0)
    .outerRadius(r);

// select paths, use arc generator to draw
var arcs = vis.selectAll("g.slice")
    .data(pie)
    .enter()
    .append("g")
    .attr("class", "slice")
    .attr("fill", "white");


arcs.append("path")
    .attr("fill", function(d, i){ return color(i); })
    .attr("d", function (d) { return arc(d); });

// add the text
arcs.append("text")
    .attr("transform", function(d){
        d.innerRadius = 0;
        d.outerRadius = r;
        d.angle = (d.startAngle + d.endAngle)/2;
        return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")translate(" + (d.outerRadius -10) +")";
    })
    .attr("text-anchor", "end")
    .text( function(d, i) {
        return data[i].label;
    });

function getRotationForNumber(val, randomOffset = false) {
    // find val in data array
    var picked = data.findIndex(o => o.value === val);
    if (picked == -1) {
        alert("Error! Unable to find " + val + " in data array.");
    }

    var ps = 360/data.length; // piece size
    var base_rotation = 360 - (picked * ps);
    // we need to add offset, because first element is at top and arrow is on right side
    var rotation = base_rotation + 90 - Math.round(ps/2);

    if (randomOffset) {
        // add random number of rotations (from 2 to 5)
        rotation += 360 * Math.floor((Math.random() * 2.5) + 2)
    }

    return rotation
}

function spinTo(val, endCallback) {
    rotation = getRotationForNumber(val, true);
    // stop any previous spin if it's running
    vis.interrupt()

    vis.transition()
    .duration(5000)
    .attrTween("transform", rotTween)
    .on("end", function(){
        endCallback(rotation);
    });
}

//make arrow
svg.append("g")
    .attr("transform", "translate(" + (w + padding.left + padding.right) + "," + ((h/2)+padding.top) + ")")
    .append("path")
    .attr("d", "M-" + (r*.15) + ",0L0," + (r*.05) + "L0,-" + (r*.05) + "Z")
    .style("fill","gold");

//draw spin circle
container.append("circle")
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("r", 195)
    .style("fill","#fff");

//spin text
container.append("text")
    .attr("x", 0)
    .attr("y", 15)
    .attr("text-anchor", "middle")
    .text("Roulette")
    .style("font-weight","bold")
    .style("font-size","30px");

function rotTween(to) {
    var i = d3.interpolate(oldrotation % 360, rotation);
    return function(t) {
        return "rotate(" + i(t) + ")";
    };
}
