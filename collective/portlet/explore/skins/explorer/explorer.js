kukit.actionsGlobalRegistry.register("explorer-togglechilds", function(oper) {
    oper.evaluateParameters(['uid'], {}, 'explorer-togglechilds action');
    var uid = oper.parms.uid;
    var uls = cssQuery("li.node-"+uid+" > ul");
    if (uls.length > 0) {
        if (hasClassName(uls[0], 'hideChildren')) {
            removeClassName(uls[0], 'hideChildren');
        } else {
            addClassName(uls[0], 'hideChildren');
        };
    };
});
kukit.commandsGlobalRegistry.registerFromAction('explorer-togglechilds',
    kukit.cr.makeSelectorCommand);
