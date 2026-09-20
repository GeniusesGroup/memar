/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"golang.org/x/crypto/sha3"

	etime "libgo/earth-time"
	"libgo/ganjine"
	"libgo/pehrest"
	"libgo/syllab"
)


var OrganizationMediaType = mediatype.New("application/vnd.sabz.city.organization+syllab", "").
	SetInfo(protocol.Software_PreAlpha, 1600109379, "").
	SetDetail(protocol.LanguageEnglish, "Organization",
		`store organization information almost for authentication and governance(blocking) purpose.
Organization doesn't have any authenticate token and persons have access by given delegate connections or just app to app connection.`,
		[]string{"Organization", "Authentication", ""}).
	Expired(0, nil)
	
const (
	organizationStructureID uint64 = 10235383584039651570
)

// Organization ---Read locale description in organizationStructure---
type Organization struct {
	WriteTime time.Time
	RequestID [16]byte // user-request domain
	ID        [16]byte `index-hash:"ObjectID,ID[daily]"` // Organization UUID
	Domain    string   `index-hash:"ObjectID"`           // unique name in the Computer world
	Status    org.OrganizationStatus
}

// SaveNew method set some data and write entire Organization record with all indexes!
func (oa *Organization) SaveNew() (err protocol.Error) {
	err = oa.Set()
	if err != nil {
		return
	}
	oa.IndexRecordIDForID()
	oa.IndexIDForRegisterTimeDaily()
	return
}

// Set method set some data and write entire Organization record!
func (oa *Organization) Set() (err protocol.Error) {
	oa.RecordStructureID = organizationStructureID
	oa.RecordSize = oa.LenAsSyllab()
	oa.WriteTime = time.Now()
	oa.OwnerAppID = protocol.OS.AppManifest().AppUUID()

	var req = ganjine.SetRecordReq{
		Type:   ganjine.RequestTypeBroadcast,
		Record: oa.ToSyllab(),
	}
	oa.RecordID = sha3.Sum256(req.Record[32:])
	copy(req.Record[0:], oa.RecordID[:])

	err = gsdk.SetRecord(&req)
	if err != nil {
		// TODO::: Handle error situation
	}
	return
}

// GetByRecordID method read all existing record data by given RecordID!
func (oa *Organization) GetByRecordID() (err protocol.Error) {
	var req = ganjine.GetRecordReq{
		RecordID:          oa.RecordID,
		RecordStructureID: organizationStructureID,
	}
	var res *ganjine.GetRecordRes
	res, err = gsdk.GetRecord(&req)
	if err != nil {
		return
	}

	err = oa.FromSyllab(res.Record)
	if err != nil {
		return
	}

	if oa.RecordStructureID != organizationStructureID {
		protocol.App.Log(log.WarnEvent(domainEnglish, "Platform collapsed!! HASH Collision Occurred on", organizationStructureID)
		err = ganjine.ErrMisMatchedStructureID
	}
	return
}

// GetLastByID method read all existing record data by given RecordID!
func (oa *Organization) GetLastByID() (err protocol.Error) {
	var IDs [][32]byte
	IDs, err = oa.FindRecordsIDByID(18446744073709551615, 1)
	if err != nil || IDs == nil {
		return
	}

	oa.RecordID = IDs[0]
	err = oa.GetByRecordID()
	return
}

/*
	-- Search Methods --
*/

// FindRecordsIDByID find RecordsID by given ID
func (oa *Organization) FindRecordsIDByID(offset, limit uint64) (RecordsID [][32]byte, err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: oa.hashIDForRecordID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	RecordsID = indexRes.IndexValues
	return
}

// FindLastIDs return org IDs register in platform in given dayNum before given WriteTime.
func (oa *Organization) FindLastIDs(offset, limit uint64, dayNum int) (RecordsID [][32]byte, err protocol.Error) {
	RecordsID = make([][32]byte, 0, limit)

	for i := 0; i < dayNum; i++ {
		var indexReq = &pehrest.HashGetValuesReq{
			IndexKey: oa.hashWriteTimeForIDDaily(),
			Offset:   offset,
			Limit:    limit,
		}
		var indexRes *pehrest.HashGetValuesRes
		indexRes, err = psdk.HashGetValues(indexReq)
		RecordsID = append(RecordsID, indexRes.IndexValues...)

		if len(RecordsID) >= int(limit) {
			break
		}

		limit -= uint64(len(indexRes.IndexValues))
		oa.WriteTime -= (24 * 60 * 60)
	}
	return
}

/*
	-- PRIMARY INDEXES --
*/

// IndexRecordIDForID save RecordID chain for oa.ID
func (oa *Organization) IndexRecordIDForID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   oa.hashIDForRecordID(),
		IndexValue: oa.RecordID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (oa *Organization) hashIDForRecordID() (hash [32]byte) {
	const field = "ID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, organizationStructureID)
	copy(buf[8:], oa.ID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

/*
	-- SECONDARY INDEXES --
*/

// IndexIDForRegisterTimeDaily index oa.WriteTime to retrieve all register Organizations on specific time in daily rate.
// Each year is 365 day that indicate we have 365 index record each year!
func (oa *Organization) IndexIDForRegisterTimeDaily() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   oa.hashWriteTimeForIDDaily(),
		IndexValue: oa.ID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Ganjine - Set Index:", err)
		}
		// TODO::: we must retry more due to record wrote successfully before this func!
	}
}

func (oa *Organization) hashWriteTimeForIDDaily() (hash [32]byte) {
	const field = "WriteTime"
	var buf = make([]byte, 16+len(field)) // 8+8
	syllab.SetUInt64(buf, 0, personAuthenticationStructureID)
	syllab.SetInt64(buf, 8, oa.WriteTime.RoundToDay())
	copy(buf[16:], field)
	return sha3.Sum256(buf)
}

/*
	-- Syllab Encoder & Decoder --
*/

func (oa *Organization) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(payload)) < oa.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}
	copy(oa.AppInstanceID[:], payload[88:])
	copy(oa.UserConnectionID[:], payload[120:])
	copy(oa.ID[:], payload[152:])
	copy(oa.SocietyID[:], payload[184:])
	copy(oa.QuiddityID[:], payload[216:])
	oa.ServicesType = OrganizationType(syllab.GetUInt8(payload, 248))
	oa.Status = OrganizationStatus(syllab.GetUInt8(payload, 249))
	return
}

func (oa *Organization) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(payload[88:], oa.AppInstanceID[:])
	copy(payload[120:], oa.UserConnectionID[:])
	copy(payload[152:], oa.ID[:])
	copy(payload[184:], oa.SocietyID[:])
	copy(payload[216:], oa.QuiddityID[:])
	syllab.SetUInt8(payload, 248, uint8(oa.ServicesType))
	syllab.SetUInt8(payload, 249, uint8(oa.Status))
	return heapIndex
}

func (oa *Organization) LenAsSyllab() uint64 {
	return uint64(oa.LenOfSyllabStack() + oa.LenOfSyllabHeap())
}
func (oa *Organization) LenOfSyllabStack() uint32     { return 250 }
func (oa *Organization) LenOfSyllabHeap() (ln uint32) { return }
