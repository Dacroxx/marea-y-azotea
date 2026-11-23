    function escapeHTML(value) {
      return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }
    function buildChronicle(key) {
      const data = chroniclesData[key];
      const mosaicEl = document.getElementById(`mosaic-${key}`);
      const videosEl = document.getElementById(`videos-${key}`);
      const items = [];
      const card = c => `<div data-editorial-card class="rounded-3xl p-6 sm:p-7 flex flex-col justify-between shadow-lg ${c.bgClass} ${c.span || ''}"><span class="text-[10px] font-bold uppercase tracking-[0.22em] ${c.tagClass}">${c.tag}</span><p class="font-fraunces italic text-base sm:text-lg leading-snug mt-3">${c.quote}</p><div class="mt-4 flex items-center gap-1.5 opacity-60"><span class="w-6 h-1 rounded-full bg-current"></span><span class="w-2 h-1 rounded-full bg-current"></span></div></div>`;
      // Redistribute ALL original editorial capsules regardless of photo count.
      const insertions = new Map();
      data.cards.forEach((c,i)=>{
        const slot = data.photos.length ? Math.min(data.photos.length-1,Math.floor((i+1)*data.photos.length/(data.cards.length+1))) : -1;
        insertions.set(slot,[...(insertions.get(slot)||[]),c]);
      });
      data.photos.forEach((photo,idx)=>{
        const index=flatLightboxPhotos.length;
        flatLightboxPhotos.push({...photo,chapterTitle:data.chapterTitle});
        const caption=escapeHTML(photo.caption), name=escapeHTML(photo.originalName);
        items.push(`<figure data-source-id="${photo.id}" data-category="${escapeHTML(photo.primaryCategory)}" class="group relative rounded-3xl overflow-hidden bg-carbon/10 shadow-md hover:shadow-2xl transition-all duration-500 ${photo.span||''}">
          <button type="button" data-open="${photo.id}" aria-label="Ampliar ${name}" class="photo-open absolute inset-0 w-full h-full text-left cursor-pointer" onclick="openLightbox(${index})">
            <img src="${driveThumb(photo.id,1200)}" data-drive-id="${photo.id}" alt="${caption}" loading="lazy" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" onerror="handleMosaicImgError(this)" />
            <span class="artistic-fallback hidden absolute inset-0 p-6 flex flex-col items-center justify-center text-center bg-gradient-to-br ${data.fallbackGrad} text-coco"><span class="font-fraunces italic text-lg">Vista previa no disponible</span><span class="text-xs mt-3">Conexión, servicio o acceso al archivo. Usa el enlace a Drive para comprobarlo.</span></span>
          </button>
          <figcaption class="absolute inset-x-0 bottom-0 p-4 pt-10 bg-gradient-to-t from-carbon/85 via-carbon/40 to-transparent text-coco opacity-95 group-hover:opacity-100 transition-opacity">
            <p class="photo-description text-xs sm:text-[13px] leading-snug font-medium drop-shadow">${caption}</p>
            <div class="file-line mt-2 text-[10px]"><span class="original-name">${name}</span><a class="photo-drive" href="${driveView(photo.id)}" target="_blank" rel="noopener noreferrer">Drive ↗</a></div>
          </figcaption></figure>`);
        (insertions.get(idx)||[]).forEach(c=>items.push(card(c)));
      });
      if (!data.photos.length) {
        items.push('<div data-empty-state class="sm:col-span-2 rounded-3xl p-7 bg-arena text-carbon flex flex-col justify-center"><h3 class="font-editorial text-2xl">Archivo visual pendiente</h3><p class="mt-3 text-sm">0 fotografías verified en este eje. Conservamos la crónica y sus voces editoriales sin atribuirlas a fotos o videos no revisados.</p></div>');
        data.cards.forEach(c=>items.push(card(c)));
      }
      mosaicEl.innerHTML=items.join('');
      videosEl.innerHTML='<div class="audiovisual-pending rounded-3xl p-7 bg-arena text-carbon border border-selva/20"><span class="text-[10px] font-bold uppercase tracking-widest text-marea">Archivo audiovisual · Pendiente</span><h4 class="font-editorial text-2xl mt-3">Memorias por revisar</h4><p class="text-sm mt-3 leading-relaxed">El archivo contiene 31 MOV no inspeccionados. No se reproducen ni se les asignan títulos, escenas o categorías hasta revisar su contenido. Esta franja conserva el lugar editorial de las memorias en movimiento.</p></div>';
    }
