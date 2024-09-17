/* For license and copyright information please see the LEGAL file in the code repository */

package chapar

import (
	"libgo/mediatype"
	"libgo/protocol"
)

/*
	Data Structure
*/

var ConnectionMediaType mediatype.MediaType

func init() {
	ConnectionMediaType.Init("application/vnd.chapar.protocol.connection+syllab")
	ConnectionMediaType.SetInfo(protocol.Software_PreAlpha, 1622176092, "")
	ConnectionMediaType.SetDetail(protocol.LanguageEnglish, "Chapar Connection",
		``,
		"",
		"",
		"",
		[]string{})
}

const (
	connectionStructureID uint64 = 11984659004635277
)

// Connection ---Read locale description in chaparConnectionStructure---
type Conn interface {
	/* Connection data */
	State() protocol.NetworkStatus
	Weight() protocol.Weight
	MTU() int
	PathToPeer() Path

	/* Peer data */
	PathFromPeer() Path // Chapar switch spec
	AlternativePaths() []Path
	ThingID() [16]byte

	/* Metrics data */
	LastUsage() protocol.Time           // Last use of this connection
	bytesSent() uint64                  // Counts the bytes of frames payload sent.
	framesSent() uint64                 // Counts sent frames.
	bytesReceived() uint64              // Counts the bytes of frames payloads received.
	framesReceived() uint64             // Counts received frames.
	failedFramesSent() uint64           // Counts failed frames receive for firewalling server from some attack types!
	failedFramesReceived() uint64       // Counts failed frames receive for firewalling server from some attack types!
	notRequestedFramesReceived() uint64 // Counts not requested frames received for firewalling server from some attack types!
}

/*
********** protocol.Ganjine interface **********
 */

func (c *Connection) saveConn() {
	// save to PersiaOS storage in caller domain scope!
	return
}

/*
-- Get Last Methods --
*/

// GetLastByPath return last connection by given c.Path from storage if exist
func (c *Connection) GetLastByPath() (err protocol.Error) {
	return
}

// GetLastByThingID return last connection by given c.ThingID from storage if exist
func (c *Connection) GetLastByThingID() (err protocol.Error) {
	return
}
