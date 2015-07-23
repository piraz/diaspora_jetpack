(function($, can) {
	'use strict';

	can.fixture({
		'GET /contacts': function() {
			return [{
				id: 1,
				name: 'Fulano de Tal',
				online: true
			}, {
				id: 2,
				name: 'Beltrano',
				online: false
			}, {
				id: 3,
				name: 'Joãozinho',
				online: true
			}];
		}
	});

	can.fixture.delay = 1000;

	var Contact = can.Model.extend({
		findAll: 'GET /contacts'
	});

	Contact.List = Contact.List.extend({
		filter: function(check) {
			var list = new this.constructor;
			this.each(function(contact) {
				if (check(contact)) {
					list.push(contact);
				}
			});
			return list;
		},
		online: function() {
			return this.filter(function(contact) {
				return contact.attr('online');
			});
		},
		onlineCount: function() {
			return this.online().attr('length');
		}
	});

	var contacts = new Contact.List({});

	var frag = can.view('#dc-chat', {
		contacts: contacts
	});

	$('body').append(frag);
})(window.jQuery, window.can);