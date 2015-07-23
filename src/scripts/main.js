(function($, can) {
	'use strict';

	function calcBoxPosition(chatBoxes) {
		var sidebarSize = $('.dc-chat-sidebar').width();
		var gutter = 15;

		if (chatBoxes.length === 0) {
			return gutter + sidebarSize;
		} else {
			var chatBoxSize = $('.dc-chat-box').width();
			return chatBoxes[chatBoxes.length - 1].attr('position') + gutter + chatBoxSize;
		}
	}

	function alreadyOpenedBox(contactId, chatBoxes) {
		var opened = false;
		chatBoxes.each(function(box) {
			if (box.attr('contact').attr('id') == contactId) {
				opened = true;
			}
		});
		return opened;
	}

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
	var chatBoxes = new can.List([]);

	can.Component.extend({
		tag: 'dc-chat-contacts',
		template: can.view('dc-chat-contacts'),
		scope: {
			openChat: function(contact, el, ev) {
				var pos = calcBoxPosition(chatBoxes);

				console.log(alreadyOpenedBox(contact.attr('id'), chatBoxes));

				if (!alreadyOpenedBox(contact.attr('id'), chatBoxes)) {
					chatBoxes.push({
						position: pos,
						contact: contact
					});
				}
			}
		}
	});

	var frag = can.view('#dc-chat', {
		contacts: contacts,
		chatBoxes: chatBoxes
	});

	$('body').append(frag);
})(window.jQuery, window.can);