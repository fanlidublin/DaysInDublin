package fanli.java.topic4.pack1;
class Link {
  public int iData;

  public Link next;

  public Link(int id) {
    iData = id;
  }

  public String toString() {
    return "{" + iData + "} ";
  }
}
