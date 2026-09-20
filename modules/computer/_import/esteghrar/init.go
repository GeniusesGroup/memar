/* For license and copyright information please see the LEGAL file in the code repository */

package esteghrar

import (
	"memar/log"
	"memar/protocol"
)

func Init() {
	if app.Manifest.DataNodes.TotalZones < 3 {
		protocol.App.Log(log.WarnEvent(domainEnglish, "ReplicationNumber set below 3! Loose write ability until two replication available again on replication failure"))
	}
}

// Deinit use to graceful stop app
func (app *appStructure) Deinit() {

}
