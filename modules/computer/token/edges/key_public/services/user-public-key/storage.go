/* For license and copyright information please see the LEGAL file in the code repository */

package upk

import (
	"golang.org/x/crypto/sha3"

	"memar/ganjine"
	"memar/pehrest"
	"memar/syllab"
)

const (
	personPublicKeyStructureID uint64 = 476305559987847614
)

var personPublicKeyStructure = ds.DataStructure{
	URN:             "urn:giti:sabz.city:data-structure:person-public-key",
	ID:              476305559987847614,
	IssueDate:       1599027351,
	ExpiryDate:      0,
	ExpireInFavorOf: "",
	Status:          protocol.Software_PreAlpha,
	Structure:       PersonPublicKey{},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Person PublicKey",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "store person Public-key (asymmetric) cryptography",
	},
	TAGS: []string{
		"",
	},
}

// PersonPublicKey ---Read locale description in personPublicKeyStructure---
type PersonPublicKey struct {
	RequestID [16]byte // user-request domain
	UserID  [16]byte `index-hash:"RecordID[pair,ThingID],ThingID"` // UUID of Person
	// ThingID   [16]byte `index-hash:"PersonID"`
	PublicKey []byte // in DER format
	Status    PersonPublicKeyStatus
}

// SaveNew method set some data and write entire Quiddity record with all indexes!
func (ppk *PersonPublicKey) SaveNew() (err protocol.Error) {
	err = ppk.Set()
	if err != nil {
		return
	}
	ppk.IndexRecordIDForPersonIDThingID()
	ppk.ListThingIDForPersonID()
	ppk.ListPersonIDForThingID()
	return
}

// Set method set some data and write entire PersonPublicKey record!
func (ppk *PersonPublicKey) Set() (err protocol.Error) {
	ppk.RecordStructureID = personPublicKeyStructureID
	ppk.RecordSize = ppk.LenAsSyllab()
	ppk.WriteTime = time.Now()
	ppk.OwnerAppID = protocol.OS.AppManifest().AppUUID()

	var req = ganjine.SetRecordReq{
		Type:   ganjine.RequestTypeBroadcast,
		Record: ppk.ToSyllab(),
	}
	ppk.RecordID = sha3.Sum256(req.Record[32:])
	copy(req.Record[0:], ppk.RecordID[:])

	err = gsdk.SetRecord(&req)
	if err != nil {
		// TODO::: Handle error situation
	}

	return
}

// GetByRecordID method read all existing record data by given RecordID!
func (ppk *PersonPublicKey) GetByRecordID() (err protocol.Error) {
	var req = ganjine.GetRecordReq{
		RecordID:          ppk.RecordID,
		RecordStructureID: personPublicKeyStructureID,
	}
	var res *ganjine.GetRecordRes
	res, err = gsdk.GetRecord(&req)
	if err != nil {
		return
	}

	err = ppk.FromSyllab(res.Record)
	if err != nil {
		return
	}

	if ppk.RecordStructureID != personPublicKeyStructureID {
		err = ganjine.ErrMisMatchedStructureID
	}
	return
}

// GetLastByPersonIDThingID method find and read last version of record by given PublicKey
func (ppk *PersonPublicKey) GetLastByPersonIDThingID() (err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: ppk.hashPersonIDThingIDForRecordID(),
		Offset:   18446744073709551615,
		Limit:    1,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	if err != nil {
		return
	}

	ppk.RecordID = indexRes.IndexValues[0]
	err = ppk.GetByRecordID()
	if err.Equal(ganjine.ErrMisMatchedStructureID) {
		protocol.App.Log(log.WarnEvent(domainEnglish, "Platform collapsed!! HASH Collision Occurred on", personPublicKeyStructureID)
	}
	return
}

/*
	-- PRIMARY INDEXES --
*/

// IndexRecordIDForPersonIDThingID save RecordID chain for PersonID+ThingID
// Call in each update to the exiting record!
func (ppk *PersonPublicKey) IndexRecordIDForPersonIDThingID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   ppk.hashPersonIDThingIDForRecordID(),
		IndexValue: ppk.RecordID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (ppk *PersonPublicKey) hashPersonIDThingIDForRecordID() (hash [32]byte) {
	const field = "PersonIDThingID"
	var buf = make([]byte, 72+len(field)) // 8+32+32
	syllab.SetUInt64(buf, 0, personPublicKeyStructureID)
	copy(buf[8:], ppk.PersonID[:])
	copy(buf[40:], ppk.ThingID[:])
	copy(buf[72:], field)
	return sha3.Sum256(buf)
}

/*
	-- SECONDARY INDEXES --
*/

// ??

/*
	-- LIST FIELDS --
*/

// ListThingIDForPersonID save ThingID chain for PersonID
// Don't call in update to an exiting record!
func (ppk *PersonPublicKey) ListThingIDForPersonID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   ppk.hashPersonIDForThingID(),
		IndexValue: ppk.ThingID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (ppk *PersonPublicKey) hashPersonIDForThingID() (hash [32]byte) {
	const field = "ListThingID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, personPublicKeyStructureID)
	copy(buf[8:], ppk.PersonID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

// ListPersonIDForThingID list PersonID chain for ThingID
// Don't call in update to an exiting record!
func (ppk *PersonPublicKey) ListPersonIDForThingID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   ppk.hashPersonIDForThingID(),
		IndexValue: ppk.PersonID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (ppk *PersonPublicKey) hashThingIDForPersonID() (hash [32]byte) {
	const field = "ListPersonID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, personPublicKeyStructureID)
	copy(buf[8:], ppk.ThingID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

/*
	-- Syllab Encoder & Decoder --
*/

func (ppk *PersonPublicKey) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(payload)) < ppk.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(ppk.AppInstanceID[:], payload[88:])
	copy(ppk.UserConnectionID[:], payload[120:])
	copy(ppk.PersonID[:], payload[152:])
	copy(ppk.ThingID[:], payload[184:])
	copy(ppk.PublicKey[:], payload[216:])
	ppk.Status = PersonPublicKeyStatus(syllab.GetUInt8(payload, 248))
}

func (ppk *PersonPublicKey) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(payload[88:], ppk.AppInstanceID[:])
	copy(payload[120:], ppk.UserConnectionID[:])
	copy(payload[152:], ppk.PersonID[:])
	copy(payload[184:], ppk.ThingID[:])
	copy(payload[216:], ppk.PublicKey[:])
	syllab.SetUInt8(payload, 248, uint8(ppk.Status))
	return heapIndex
}

func (ppk *PersonPublicKey) LenAsSyllab() uint64 {
	return uint64(ppk.LenOfSyllabStack() + ppk.LenOfSyllabHeap())
}
func (ppk *PersonPublicKey) LenOfSyllabStack() uint32     { return 249 }
func (ppk *PersonPublicKey) LenOfSyllabHeap() (ln uint32) { return }

/*
	-- Record types --
*/

// PersonPublicKeyStatus use to indicate PersonPublicKey record status
type PersonPublicKeyStatus uint8

// PersonPublicKey status
const (
	PersonPublicKeyIssueByPassword PersonPublicKeyStatus = iota
	PersonPublicKeyIssueByPasswordAndOTP
	PersonPublicKeyIssueByPasswordAndIdentification
	PersonPublicKeyIssueByPasswordAndOTPAndIdentification
	PersonPublicKeyExpired
	PersonPublicKeyRevoked
)
