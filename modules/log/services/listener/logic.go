/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/protocol"
)

type Listeners struct {
	all       []protocol.LogListener
	listeners map[listenerKey]protocol.LogListener
}

type listenerKey struct {
	level  protocol.LogType
	domain string
}

func (l *Listeners) sendToListeners(event protocol.LogEvent) {
	var level = event.Level()
	var domain = event.Domain()

	for i := 0; i < len(l.all); i++ {
		l.all[i].LogEventHandler(event)
	}

	var key = listenerKey{
		level:  level,
		domain: domain,
	}
	var ls = l.listeners[key]
	if ls != nil {
		ls.LogEventHandler(event)
	}

	key = listenerKey{
		level: level,
		// domain: "",
	}
	ls = l.listeners[key]
	if ls != nil {
		ls.LogEventHandler(event)
	}

	key = listenerKey{
		// level:  protocol.LogEvent_Unset,
		domain: domain,
	}
	ls = l.listeners[key]
	if ls != nil {
		ls.LogEventHandler(event)
	}
}

func (l *Listeners) RegisterListener(level protocol.LogType, domain string, ll protocol.LogListener) (err protocol.Error) {
	if level == protocol.LogEvent_Unset && domain == "" {
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

func (l *Listeners) DeregisterListener(level protocol.LogType, domain string, ll protocol.LogListener) (err protocol.Error) {
	if level == protocol.LogEvent_Unset && domain == "" {
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
