/* For license and copyright information please see the LEGAL file in the code repository */

package user

import (
	"crypto/rand"
	"io"

	"memar/binary"
	"memar/time/duration"
	time_p "memar/time/protocol"
	"memar/time/unix"

	user_p "org/modules/identity/user/protocol"
)

func NewID(userType user_p.Type) (id UUID) {
	id.Init(userType)
	return
}

// 0...7 >> second elapsed
// 8...11 >> nano second elapsed
// 12...12 >> type
// 13...15 >> random id
type UUID [16]byte

// Init fill UUID to new user ID with desire user type.
func (self *UUID) Init(userType user_p.Type) {
	var now = unix.Now()
	self.setSecondElapsed(now.SecondElapsed())
	self.setNanoInSecondElapsed(now.NanoInSecondElapsed())
	self[12] = byte(userType)
	// TODO::: `moved to heap: id` Is it any way to prevent heap alloc??
	// rand.Read(self[13:])
	io.ReadAtLeast(rand.Reader, self[13:], 3)
}

func (self UUID) UUID() user_p.UUID { return user_p.UUID(self) }
func (self UUID) Type() user_p.Type { return user_p.Type(self[8]) }
func (self UUID) ID() [3]byte       { return self.id() }
func (self UUID) ExistenceTime() time_p.Time {
	var time unix.Time
	time.ChangeTo(self.secondElapsed(), self.nanoSecondElapsed())
	return &time
}

func (self UUID) id() (id [3]byte) { copy(self[:], self[13:]); return }
func (self UUID) secondElapsed() duration.Second {
	return duration.Second(binary.LittleEndian.Uint64(self[0:]))
}
func (self UUID) nanoSecondElapsed() duration.NanoInSecond {
	return duration.NanoInSecond(binary.LittleEndian.Uint32(self[8:]))
}
func (self *UUID) setSecondElapsed(sec duration.Second) {
	binary.LittleEndian.PutUint64(self[0:], uint64(sec))
}
func (self *UUID) setNanoInSecondElapsed(nsec duration.NanoInSecond) {
	binary.LittleEndian.PutUint32(self[8:], uint32(nsec))
}
