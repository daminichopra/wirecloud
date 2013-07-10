/*
*     (C) Copyright 2008 Telefonica Investigacion y Desarrollo
*     S.A.Unipersonal (Telefonica I+D)
*
*     This file is part of Morfeo EzWeb Platform.
*
*     Morfeo EzWeb Platform is free software: you can redistribute it and/or modify
*     it under the terms of the GNU Affero General Public License as published by
*     the Free Software Foundation, either version 3 of the License, or
*     (at your option) any later version.
*
*     Morfeo EzWeb Platform is distributed in the hope that it will be useful,
*     but WITHOUT ANY WARRANTY; without even the implied warranty of
*     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*     GNU Affero General Public License for more details.
*
*     You should have received a copy of the GNU Affero General Public License
*     along with Morfeo EzWeb Platform.  If not, see <http://www.gnu.org/licenses/>.
*
*     Info about members and contributors of the MORFEO project
*     is available at
*
*     http://morfeo-project.org
 */


/**
 * @abstract
 *
 * This class has the common properties of every connectable object of the wiring module.
 * The other connectable classes from the wiring module will inherit from this class.
 *
 * @param name name of the connectable
 * @param type data type managed by this connectable
 * @param friendCode friendCode of this connectable
 * @param id id of this connectable
 */
function wConnectable (name, type, friendCode, id) {
    this.id = id;
}

/**
 * @private
 *
 * Stablish a new value for this <code>wConnectable</code> but without
 * propagating any event.
 */
wConnectable.prototype._annotate = function(value, source, options) {
    var funcName = '_annotate';
    var msg = gettext("Unimplemented function: %(funcName)s");
    msg = interpolate(msg, {funcName: funcName}, yes);
    LogManagerFactory.getInstance().log(msg);
    return;
}

wConnectable.prototype.getValue = function() {
    var funcName = 'getValue';
    var msg = gettext("Unimplemented function: %(funcName)s");
    msg = interpolate(msg, {funcName: funcName}, yes);
    LogManagerFactory.getInstance().log(msg);
    return;
}

wConnectable.prototype.getId = function() {
    return this.id;
}

wConnectable.prototype.getFinalSlots = function() {
    return null;
}

/**
 * Disconnects this <code>wConnectable</code> from all the
 * <code>wConnectables</code> this is connected to.
 */
wConnectable.prototype.fullDisconnect = function() {
    var funcName = 'fullDisconnect';
    var msg = gettext("Unimplemented function: %(funcName)s");
    msg = interpolate(msg, {funcName: funcName}, yes);
    LogManagerFactory.getInstance().log(msg);
    return;
}

/**
 * This method must be called to avoid memory leaks caused by circular
 * references.
 */
wConnectable.prototype.destroy = function () {
    this.fullDisconnect();
}



/**
 * @abstract
 *
 * This class represents every object in which the transmission is ended
 */
function wOut(name, type, friendCode, id) {
    wConnectable.call(this, name, type, friendCode, id);
    this.inouts = new Array();
}

wOut.prototype = new wConnectable();

wOut.prototype._annotate = function(value, source, options) {
}

/**
 * @private
 *
 * This method must be used only by the connectables code. If you like to
 * connect an wOut to an wInOut, you should call to the connect method of the
 * wInOut intance.
 */
wOut.prototype._addInput = function(inout) {
    this.inouts.push(inout);
}

wOut.prototype.fullDisconnect = function() {
    // Disconnecting inouts
    var inouts = this.inouts.clone();
    for (var i = 0; i < inouts.length; ++i)
        inouts[i].disconnect(this);
}

/**
 * @abstract
 *
 * This class represents every object which may initialize one transmission
 * through the wiring module.
 *
 * @param name
 * @param type
 * @param friendCode
 * @param id
 */
function wIn(name, type, friendCode, id) {
    wConnectable.call(this, name, type, friendCode, id);
    this.outputs = new Array();
}
wIn.prototype = new wConnectable();

wIn.prototype.connect = function(out) {
    this.outputs.push(out);

    out._addInput(this);
}

wIn.prototype.disconnect = function(out) {
    if (this.outputs.getElementById(out.getId()) == out) {
        this.outputs.remove(out);
    }
}

wIn.prototype.fullDisconnect = function() {
    // Outputs
    var outputs = this.outputs.clone();
    for (var i = 0; i < outputs.length; ++i)
        this.disconnect(outputs[i]);
}

/**
 * Sets the value for this <code>wIn</code>. Also, this method propagates this
 * new value to the output connectables.
 */
wIn.prototype.propagate = function(value, options) {
    options = Object.extend({
        initial: false
    }, options);

    for (var i = 0; i < this.outputs.length; ++i)
        this.outputs[i]._annotate(value, this, options);

    for (var i = 0; i < this.outputs.length; ++i)
        this.outputs[i].propagate(value, options);
}

wIn.prototype.getFinalSlots = function() {
    var slots = [];
    for (var i = 0; i < this.outputs.length; ++i) {
        var currentSlots = this.outputs[i].getFinalSlots();
        if (currentSlots && currentSlots.length > 0)
            slots = slots.concat(currentSlots);
    }

    return slots;
}
