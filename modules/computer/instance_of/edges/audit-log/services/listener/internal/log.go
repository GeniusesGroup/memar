/* For license and copyright information please see the LEGAL file in the code repository */

package log

import (
	"memar/log"
	log_p "memar/log/protocol"
	"memar/protocol"
)

type Logger struct{}

func (l *Logger) Log(event log_p.Event) (err error_p.Error) {
	log.Logger.DispatchEvent(event)
	// Due to LogEvent is not cancelable, we don't need to check event.DefaultPrevented() before save log.
	// if event.DefaultPrevented() {}
	err = l.saveEvent(event)
	return
}

func (l *Logger) saveEvent(event log_p.Event) (err error_p.Error) {
	if !CheckLevelEnabled(event.Level()) {
		return
	}

	// TODO::: First save locally as cache to reduce network trip for non important data??
	// TODO::: limit log sizes to defeat attacks??

	// TODO::: Each day, Save logs to storage(mediatype.LOG.ID()) with NodeID as object ID
	// protocol.STG.Objects().
	return
}

func CheckLevelEnabled(level log_p.Level) bool {
	return protocol.LogMode&level != 0
}
