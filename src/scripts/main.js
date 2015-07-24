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

	can.mustache('dc-chat', '<div class="dc-chat-sidebar"> \
											<div class="dc-chat-title"> \
												<i class="fa fa-comments"></i> Chat \
												<span class="badge dc-chat-title-badge">{{contacts.onlineCount}}</span> \
											</div> \
											<dc-chat-contacts></dc-chat-contacts> \
										</div> \
										<div class="dc-chat-boxes"> \
											{{#each chatBoxes}} \
												<dc-chat-box></dc-chat-box> \
											{{/each}} \
										</div>');

	can.mustache('dc-chat-contacts', '<div class="dc-chat-contacts"> \
													{{#each contacts}} \
														<div class="dc-chat-contact" can-click="openChat"> \
															<img class="dc-chat-contact-avatar" src="http://placehold.it/30x30" alt="50x50"> \
															<span class="dc-chat-contact-name">{{name}}</span> \
															{{#if online}} \
																<i class="fa fa-circle dc-chat-contact-online"></i> \
															{{/if}} \
														</div> \
													{{/each}} \
												</div>');

	can.mustache('dc-chat-box', '<div class="dc-chat-box" id="{{boxId}}" style="right:{{position}}px"> \
												<div class="dc-chat-box-header"> \
													<i class="fa fa-comment"></i> {{contact.name}} \
													<button class="dc-chat-box-header-btn" can-click="closeChat"> \
														<i class="fa fa-times"></i> \
													</button> \
												</div> \
												<div class="dc-chat-box-msgs"> \
													{{#each msgs}} \
														<div class="dc-chat-msg-row"> \
															<div class="dc-chat-msg {{#if me}}me{{else}}notme{{/if}}">{{msg}}</div> \
														</div> \
													{{/each}} \
												</div> \
												<div class="dc-chat-box-input"> \
													<input type="text" autofocus="" placeholder="Envie uma mensagem" can-enter="addMsg"> \
												</div> \
											</div>');

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