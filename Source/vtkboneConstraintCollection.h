/*=========================================================================

  Copyright 2010-2016, Numerics88 Solutions Ltd.
  http://www.numerics88.com/

  Copyright (c) Eric Nodwell and Steven K. Boyd
  See Copyright.txt for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.
=========================================================================*/

// .NAME vtkboneConstraintCollection - maintain an unordered list of dataarray objects
// .SECTION Description
// vtkboneConstraintCollection is an object that creates and manipulates lists of
// datasets.
// .SECTION See Also
// vtkCollection vtkboneConstraint

#ifndef __vtkboneConstraintCollection_h
#define __vtkboneConstraintCollection_h

#include "vtkCollection.h"
#include "vtkboneWin32Header.h"

#include "vtkboneConstraint.h" // Needed for inline methods

class VTKBONE_EXPORT vtkboneConstraintCollection : public vtkCollection
{
public:
  static vtkboneConstraintCollection *New();
  vtkTypeMacro(vtkboneConstraintCollection, vtkCollection);

  // Description:
  // Add a dataset to the list.
  void AddItem(vtkboneConstraint *ds)
    {this->vtkCollection::AddItem(ds);}

  // Description:
  // Get the next dataset in the list.
  vtkboneConstraint *GetNextItem() {
    return static_cast<vtkboneConstraint *>(this->GetNextItemAsObject());};

  // Description:
  // Get the ith dataset in the list.
  vtkboneConstraint *GetItem(int i) {
    return static_cast<vtkboneConstraint *>(this->GetItemAsObject(i));};

  // Description:
  // Get the dataset with specified name.
  vtkboneConstraint *GetItem(const char* name);

  // Description:
  // Remove an named Collection from the list. Removes the first object found, not
  // all occurrences. If no object found, list is unaffected.  See warning
  // in description of RemoveItem(int).
  void RemoveItem(const char* name)
    { this->vtkCollection::RemoveItem(this->GetItem(name)); }

  // Description:
  // Get next object in collection.
  vtkboneConstraint *GetNextConstraint() {
    return static_cast<vtkboneConstraint *>(this->GetNextItemAsObject());};

  //BTX
  // Description:
  // Reentrant safe way to get an object in a collection. Just pass the
  // same cookie back and forth.
  vtkboneConstraint *GetNextConstraint(vtkCollectionSimpleIterator &cookie) {
    return static_cast<vtkboneConstraint *>(this->GetNextItemAsObject(cookie));};
  //ETX

protected:
  vtkboneConstraintCollection() {};
  ~vtkboneConstraintCollection() {};


private:
  // hide the standard AddItem from the user and the compiler.
  void AddItem(vtkObject *o) { this->vtkCollection::AddItem(o); };

private:
  vtkboneConstraintCollection(const vtkboneConstraintCollection&);  // Not implemented.
  void operator=(const vtkboneConstraintCollection&);  // Not implemented.
};


#endif
