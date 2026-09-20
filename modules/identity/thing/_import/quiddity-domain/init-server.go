/* For license and copyright information please see the LEGAL file in the code repository */

package qd

import (
	"libgo/protocol"

	gs "quiddity-domain/services/get"
	rs "quiddity-domain/services/register"
)

// RegisterServices will register services in the application.
func RegisterServices() {
	protocol.App.RegisterService(&rs.Service)
	protocol.App.RegisterService(&gs.Service)
}
