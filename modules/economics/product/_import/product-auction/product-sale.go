/* For license and copyright information please see the LEGAL file in the code repository */

package authorization

import (
	"../json"
	"../protocol"
	"../syllab"
)

// Product store needed data to authorize product as auction or any other order type
type Product struct {
	AllowUserID   [32]byte `index-hash:"ID" json:",string"` // If 0 means this sale is not just for specific UserID! can be any OrgID e.g. DistributionCenterID
	AllowUserType protocol.UserType
	AllowWeekdays protocol.Weekdays
	AllowDayHours protocol.DayHours
	GroupID       [32]byte `index-hash:"ID" json:",string"` // it can be 0 and means sale is global!
	MinNumBuy     uint64   // Minimum number to buy in this auction to use for sale-off(Discount)
	StockNumber   uint64   // 0 for unlimited until related product exist to sell!
	LiveUntil     protocol.TimeUnixSec
}

// GiveFullAccess set some data to given AccessControl to be full access
func (p *Product) GiveFullAccess() {
	p.AllowUserType = protocol.UserType_All
	p.AllowWeekdays = protocol.WeekdaysAll
	p.AllowDayHours = protocol.DayHoursAll
}

// FromSyllab decode syllab to given Product
func (p *Product) FromSyllab(buf []byte, stackIndex uint32) (err protocol.Error) {
	// var add, ln uint32
	// var tempSlice []byte

	if uint32(len(buf)) < p.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(p.AllowUserID[:], buf[stackIndex:])
	p.AllowUserType = protocol.UserType(syllab.GetUInt8(buf, stackIndex+32))
	p.AllowWeekdays = protocol.Weekdays(syllab.GetUInt8(buf, stackIndex+33))
	p.AllowDayHours = protocol.DayHours(syllab.GetUInt32(buf, stackIndex+34))
	copy(p.GroupID[:], buf[stackIndex+38:])
	p.MinNumBuy = syllab.GetUInt64(buf, stackIndex+70)
	p.StockNumber = syllab.GetUInt64(buf, stackIndex+78)
	p.LiveUntil = protocol.TimeUnixSec(syllab.GetInt64(buf, stackIndex+86))
	return
}

// ToSyllab encode given Product to syllab format
func (p *Product) ToSyllab(buf []byte, stackIndex uint32) {
	copy(buf[stackIndex:], p.AllowUserID[:])
	syllab.SetUInt8(buf, stackIndex+32, uint8(p.AllowUserType))
	syllab.SetUInt8(buf, stackIndex+33, uint8(p.AllowWeekdays))
	syllab.SetUInt32(buf, stackIndex+34, uint32(p.AllowDayHours))
	copy(buf[stackIndex+38:], p.GroupID[:])
	syllab.SetUInt64(buf, stackIndex+70, p.MinNumBuy)
	syllab.SetUInt64(buf, stackIndex+78, p.StockNumber)
	syllab.SetInt64(buf, stackIndex+86, int64(p.LiveUntil))
}

// LenOfSyllabStack return stack length of Product
func (p *Product) LenOfSyllabStack() uint32 {
	return 94
}

// LenOfSyllabHeap return heap length of Product
func (p *Product) LenOfSyllabHeap() (ln uint32) {
	return
}

// LenAsSyllab return whole length of Product
func (p *Product) LenAsSyllab() uint64 {
	return uint64(p.LenOfSyllabStack() + p.LenOfSyllabHeap())
}

// FromJSON decode json to given Product
func (p *Product) FromJSON(decoder *json.DecoderUnsafeMinified) (err protocol.Error) {
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "AllowUserID":
			err = decoder.DecodeByteArrayAsBase64(p.AllowUserID[:])
		case "AllowUserType":
			var num uint8
			num, err = decoder.DecodeUInt8()
			p.AllowUserType = protocol.UserType(num)
		case "AllowWeekdays":
			var num uint8
			num, err = decoder.DecodeUInt8()
			p.AllowWeekdays = protocol.Weekdays(num)
		case "AllowDayHours":
			var num uint32
			num, err = decoder.DecodeUInt32()
			p.AllowDayHours = protocol.DayHours(num)
		case "GroupID":
			err = decoder.DecodeByteArrayAsBase64(p.GroupID[:])
		case "MinNumBuy":
			p.MinNumBuy, err = decoder.DecodeUInt64()
		case "StockNumber":
			p.StockNumber, err = decoder.DecodeUInt64()
		case "LiveUntil":
			var num int64
			num, err = decoder.DecodeInt64()
			p.LiveUntil = protocol.TimeUnixSec(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		decoder.FindEndToken()
		if decoder.Token == '}' {
			decoder.Offset(1)
			return
		}
	}
	return
}

// ToJSON encode given Product to json format.
func (p *Product) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"AllowUserID":"`)
	encoder.EncodeByteSliceAsBase64(p.AllowUserID[:])

	encoder.EncodeString(`","AllowUserType":`)
	encoder.EncodeUInt8(uint8(p.AllowUserType))

	encoder.EncodeString(`,"AllowWeekdays":`)
	encoder.EncodeUInt8(uint8(p.AllowWeekdays))

	encoder.EncodeString(`,"AllowDayHours":`)
	encoder.EncodeUInt32(uint32(p.AllowDayHours))

	encoder.EncodeString(`,"GroupID":"`)
	encoder.EncodeByteSliceAsBase64(p.GroupID[:])

	encoder.EncodeString(`","MinNumBuy":`)
	encoder.EncodeUInt64(p.MinNumBuy)

	encoder.EncodeString(`,"StockNumber":`)
	encoder.EncodeUInt64(p.StockNumber)

	encoder.EncodeString(`,"LiveUntil":`)
	encoder.EncodeInt64(int64(p.LiveUntil))

	encoder.EncodeByte('}')
	return encoder.Buf
}

// LenAsJSON return json needed len to encode!
func (p *Product) LenAsJSON() (ln int) {
	ln = 455
	return
}
