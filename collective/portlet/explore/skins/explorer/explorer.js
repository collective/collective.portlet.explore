/*
jQuery portletNavigationTree plugin
	Collapsible/expandable navigation tree.
*/

(function($) {
	
	$.fn.portletNavigationTree = function(options){
		return this.each(function(){
			
			var element = $(this);
			
			// find portlet hash from portlet wrapper
			var portletWrapper = $(this).closest(".portletWrapper");
			
			var portletHash = portletWrapper[0] ? portletWrapper[0].id.replace("portletwrapper-","") : "";
			if (!portletHash) return;
			
			// observe clicks on toggle buttons
			$("span.toggleNode", element).live("click", loadNode);
			$("span.expandedNode", element).live("click", toggleNode);
			
			// Expands or collapses a node of which sub-items already have been loaded.
			function toggleNode(event){
				var twistie = $(this);
				
				// find ul element
				var ul = $(this).closest("a").next("ul");
				if (!ul) return;
				
				// toggle class names
				if (twistie.hasClass("showChildren")){
					ul.removeClass("hideChildren");
					twistie.removeClass("showChildren");
				} else {
					ul.addClass("hideChildren");
					twistie.addClass("showChildren");
				}
				
				// prevent default action of event
				event.preventDefault();
			}
			
			// Loads the sub-items of a node.
			function loadNode(event){
			
				// prevent default action of event
				event.preventDefault();
				
				// find the li element of the clicked node
				var node = $(this).closest("li");
				
				if (node.hasClass("nodeLoading")) return;
				
				// get node uid
				var uidClassName = node[0].className.match(/node-(\w+)/);
				var uid = uidClassName ? uidClassName[1] : null;
				if (!uid) return;
				
				// data to send with request
				var data = {
					portlethash : portletHash,
					uid : uid
				};
				
				// add nodeLoading class
				node.addClass("nodeLoading");
				
				// send request
				$.post("expandNode", data, function(html){
					node.replaceWith(html);
				});
			}
		});
	};
	
	// apply portletNavigationTree plugin on elements with class name "portletNavigationTree" after DOM has loaded
	$(function(){
		$(".portletNavigationTree").portletNavigationTree();
	});
	
})(jQuery);