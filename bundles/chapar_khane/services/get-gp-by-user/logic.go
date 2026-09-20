/* For license and copyright information please see the LEGAL file in the code repository */

package ggbuService

import (
	net_p "memar/net/protocol"
)

// GetGPAddress use to make new connection by ECC algorithm.
func GetGPAddress(sk net_p.Socket) {
	// Make Connection.EncryptionKey by ECC algorithm with :
	// req.UserPublicKey
	// RunningServerData.PublicKeyCryptography.PrivateKey

	// Check server allow to register guest connection and max guest connection availability

	// If everything go well register connection
	// s.Connections.RegisterConnection(sk)
}
