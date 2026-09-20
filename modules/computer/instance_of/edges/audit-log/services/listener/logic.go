/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	event_p "memar/process/event/protocol"
	"memar/protocol"
)

type Listeners struct {
	all       []event_p.EventListener
	listeners map[listenerKey]event_p.EventListener
}

type listenerKey struct {
	level  log_p.Level
	domain protocol.MediaType
}

func (l *Listeners) sendToListeners(event log_p.Event) {
	var level = event.Level()
	var domain = event.Domain()

	for i := 0; i < len(l.all); i++ {
		l.all[i].EventHandler(event)
	}

	var key = listenerKey{
		level:  level,
		domain: domain,
	}
	var ls = l.listeners[key]
	if ls != nil {
		ls.EventHandler(event)
	}

	key = listenerKey{
		level: level,
		// domain: "",
	}
	ls = l.listeners[key]
	if ls != nil {
		ls.EventHandler(event)
	}

	key = listenerKey{
		// level:  log_p.Level_Unset,
		domain: domain,
	}
	ls = l.listeners[key]
	if ls != nil {
		ls.EventHandler(event)
	}
}

func (l *Listeners) RegisterListener(level log_p.Level, domain protocol.MediaType, ll event_p.EventListener) (err error_p.Error) {
	if level == log_p.Level_Unset && domain == nil {
		l.all = append(l.all, ll)
		return
	}

	var key = listenerKey{
		level:  level,
		domain: domain,
	}
	// TODO::: need lock??
	l.listeners[key] = ll
	return
}

func (l *Listeners) DeregisterListener(level log_p.Level, domain protocol.MediaType, ll event_p.EventListener) (err error_p.Error) {
	if level == log_p.Level_Unset && domain == nil {
		var ln = len(l.all)
		for i := 0; i < ln; i++ {
			if l.all[i] == ll {
				copy(l.all[i:], l.all[i+1:])
				l.all = l.all[:ln-1]
				break
			}
		}
		return
	}

	var key = listenerKey{
		level:  level,
		domain: domain,
	}
	// TODO::: need lock??
	delete(l.listeners, key)
	return
}
