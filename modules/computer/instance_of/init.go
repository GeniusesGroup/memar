/* For license and copyright information please see the LEGAL file in the code repository */

package instance_of

import (
	"memar/operation/services"
)

const (
	DomainName = "node.protocol"
)

// registerServices use to initialize services and register them in the application.
func registerServices() {
	services.Register(&GetNodeDetailsService)
	// protocol.App.RegisterService()
}

// RequestType indicate request type!
type RequestType uint8

// Services request types
const (
	RequestTypeStandalone RequestType = iota
	RequestTypeBroadcast
)
