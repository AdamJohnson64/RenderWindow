////////////////////////////////////////////////////////////////////////////////
// GL Mesh Rendering
////////////////////////////////////////////////////////////////////////////////

function glRenderMesh(mesh) {
  // Position
  gl.bindBuffer(gl.ARRAY_BUFFER, mesh.id_vertex);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 3, gl.FLOAT, gl.FALSE, 12, 0);
  // Normal
  gl.bindBuffer(gl.ARRAY_BUFFER, mesh.id_normal);
  gl.enableVertexAttribArray(1);
  gl.vertexAttribPointer(1, 3, gl.FLOAT, gl.FALSE, 12, 0);
  // Draw
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, mesh.id_index);
  gl.drawElements(gl.TRIANGLES, 3 * mesh.triangle_count, gl.UNSIGNED_SHORT, 0);
}