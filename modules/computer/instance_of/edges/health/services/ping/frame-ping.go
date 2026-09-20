/* For license and copyright information please see the LEGAL file in the code repository */

package srpc

import (
	net_p "memar/net/protocol"
	"memar/syllab"
)

/*
	type pingFrame struct {
		ID int64 // Usually unix time
	}
*/
type pingFrame []byte

func (f pingFrame) ID() int64 { return syllab.GetInt64(f, 0) }

//memar:impl memar/protocol.Network_Frame
func (f pingFrame) NextFrame() []byte { return f[8:] }

func (f pingFrame) Do(sk net_p.Socket) (err error_p.Error) {
	return
}
