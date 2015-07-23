(function($, can, CryptoJS) {
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
	var chatBoxes = new can.List([]);
	var chatMsgs = new can.List([]);

	can.Component.extend({
		tag: 'dc-chat-contacts',
		template: can.view('dc-chat-contacts'),
		viewModel: {
			openChat: function(contact, el, ev) {
				var boxId = CryptoJS.MD5(contact.attr('name')).toString();
				var chatBox = $('#' + boxId);

				if (chatBox.length) {
					chatBox.show();
				} else {
					chatBoxes.push({
						boxId: boxId,
						contact: contact
					});
				}

				$('#' + boxId).find('.dc-chat-box-input > input').focus();
			}
		}
	});

	can.Component.extend({
		tag: 'dc-chat-box',
		template: can.view('dc-chat-box'),
		viewModel: {
			msgs: [],
			closeChat: function(chatBox, el) {
				el.parents('.dc-chat-box').hide();
			},
			addMsg: function(chatBox, el) {
				if(el.val().length > 0) {
					this.msgs.push({
						msg: el.val(),
						me: true
					});

					this.msgs.push({
						msg: 'Received: ' + el.val(),
						me: false
					});

					var chatRow = $('.dc-chat-msg-row');
					var scrollSize = chatRow.length * chatRow.height();

					$('.dc-chat-box-msgs').scrollTop(scrollSize);

					el.val('');
				}
			}
		}
	});

	var frag = can.view('#dc-chat', {
		contacts: contacts,
		chatBoxes: chatBoxes
	});

	$('body').append(frag);
})(window.jQuery, window.can, window.CryptoJS);